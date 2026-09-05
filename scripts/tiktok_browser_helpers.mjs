const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function hasFn(value) {
  return typeof value === "function";
}

function trimmedText(node) {
  return (node?.innerText || node?.textContent || "").trim();
}

async function clickWhenAvailable(locator, { timeoutMs = 15000, force = false } = {}) {
  if (!locator || !hasFn(locator.count)) return false;
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const count = await locator.count().catch(() => 0);
    if (count > 0) {
      const visible = await locator.first().isVisible().catch(() => false);
      if (visible) {
        await locator.first().click({ force }).catch(() => {});
        return true;
      }
    }
    await delay(500);
  }
  return false;
}

async function waitForUploadControl(tab, timeoutMs = 30000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const ready = await tab.playwright.evaluate(() => {
      const text = (document.body?.innerText || "").replace(/\u00a0/g, " ");
      return text.includes("動画を選択") || text.includes("Upload") || text.includes("投稿予約");
    });
    if (ready) return;
    await delay(500);
  }
  throw new Error("TikTok upload control did not render");
}

async function findTextPoint(tab, text) {
  return tab.playwright.evaluate((searchText) => {
    const candidates = [...document.querySelectorAll("*")].filter((el) => {
      const candidateText = (el.innerText || el.textContent || "").trim().replace(/\u00a0/g, " ");
      if (!candidateText) return false;
      return candidateText === searchText || candidateText.includes(searchText);
    });
    const target = candidates.find((el) => {
      const style = getComputedStyle(el);
      const box = el.getBoundingClientRect();
      const interactive = el.tagName === "BUTTON" || (el.getAttribute("role") === "button") || style.cursor === "pointer" || el.onclick;
      return box.width > 4 && box.height > 4 && (interactive || el.tagName === "A");
    }) || candidates[0];
    if (!target) return null;
    const rect = target.getBoundingClientRect();
    return { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };
  }, text);
}

async function clickText(tab, text, { force = true, timeoutMs = 8000 } = {}) {
  const play = tab.playwright;
  const textMatchers = [text, text.trim()];

  for (const matcher of textMatchers) {
    if (hasFn(play.getByText)) {
      try {
        const nodeExact = play.getByText(matcher, { exact: true });
        const hasExact = await nodeExact.isVisible({ timeout: 1200 }).catch(() => false);
        if (hasExact) {
          await nodeExact.click({ force }).catch(() => {});
          return true;
        }
      } catch {
        // continue
      }
      try {
        const nodeLoose = play.getByText(matcher);
        const hasLoose = await nodeLoose.isVisible({ timeout: 1200 }).catch(() => false);
        if (hasLoose) {
          await nodeLoose.first().click({ force }).catch(() => {});
          return true;
        }
      } catch {
        // continue
      }
    }

    if (hasFn(play.getByRole)) {
      for (const role of ["button", "link", "checkbox", "switch", "radio", "textbox"]) {
        try {
          const node = play.getByRole(role, { name: matcher, exact: true });
          const hasNode = await node.isVisible({ timeout: 1200 }).catch(() => false);
          if (hasNode) {
            await node.click({ force }).catch(() => {});
            return true;
          }
        } catch {
          // continue
        }
      }
    }

    if (hasFn(play.locator)) {
      const locator = play.locator(`button, [role='button'], a, [role='link'], [role='radio'], [role='switch'], [role='textbox'], [role='checkbox']`);
      try {
        const items = await locator.allTextContents().catch(() => []);
        for (let i = 0; i < items.length; i += 1) {
          const value = (items[i] || "").trim();
          if (!value.includes(matcher)) continue;
          const target = locator.nth(i);
          const visible = await target.isVisible().catch(() => false);
          if (!visible) continue;
          await target.click({ force }).catch(() => {});
          return true;
        }
      } catch {
        // continue
      }
    }
  }

  const point = await findTextPoint(tab, text);
  if (!point) return false;
  try {
    await tab.cua.move(point);
  } catch {
    // no-op
  }
  await tab.cua.click(point);
  await delay(150);
  return true;
}

async function setTextValueBySelectors(play, selectors, value) {
  if (hasFn(play.locator)) {
    for (const selector of selectors) {
      try {
        const locator = play.locator(selector);
        const count = await locator.count().catch(() => 0);
        if (!count) continue;
        const field = locator.first();
        const visible = await field.isVisible().catch(() => false);
        if (!visible) continue;
        const method = field.fill;
        if (hasFn(method)) {
          await field.click({ force: true }).catch(() => {});
          await method.call(field, value).catch(() => {});
          return true;
        }
      } catch {
        // try next
      }
    }
  }

  const matched = await play.evaluate((selectorCandidates, text) => {
    const selectors = selectorCandidates;
    const visible = (el) => {
      const rect = el.getBoundingClientRect();
      return rect.width > 2 && rect.height > 2;
    };
    for (const selector of selectors) {
      const candidates = [...document.querySelectorAll(selector)];
      for (const candidate of candidates) {
        if (!visible(candidate)) continue;
        if (candidate.tagName === "INPUT" || candidate.tagName === "TEXTAREA") {
          candidate.focus();
          candidate.value = text;
          candidate.dispatchEvent(new Event("input", { bubbles: true }));
          candidate.dispatchEvent(new Event("change", { bubbles: true }));
          return true;
        }
        if ((candidate.contentEditable || candidate.getAttribute("contenteditable") === "true")) {
          candidate.focus();
          candidate.textContent = text;
          candidate.innerText = text;
          candidate.dispatchEvent(new Event("input", { bubbles: true }));
          candidate.dispatchEvent(new Event("change", { bubbles: true }));
          return true;
        }
      }
    }
    return false;
  }, selectors, value);

  return Boolean(matched);
}

async function setCaption(tab, caption) {
  const selectors = [
    "textarea",
    "[contenteditable='true']",
    "[role='textbox']",
    "[role='combobox']",
  ];
  const deadline = Date.now() + 30000;
  let ok = false;
  while (!ok && Date.now() < deadline) {
    ok = await setTextValueBySelectors(tab.playwright, selectors, caption);
    if (ok) break;
    await delay(500);
  }
  if (!ok) throw new Error("caption input not found or not writable");
}

async function setFileForUpload(tab, videoPath, shortId) {
  const play = tab.playwright;
  const fileInput = play.locator ? play.locator("input[type='file']") : null;
  const inputCount = fileInput ? await fileInput.count().catch(() => 0) : 0;
  await clickText(tab, "破棄する", { timeoutMs: 1000 }).catch(() => {});
  await clickText(tab, "続ける", { timeoutMs: 800 }).catch(() => {});

  const trySetInputFiles = async () => {
    const currentFileInput = play.locator ? play.locator("input[type='file']") : null;
    const currentCount = currentFileInput ? await currentFileInput.count().catch(() => 0) : 0;
    if (!currentCount) return false;
    try {
      const firstInput = currentFileInput.first();
      if (hasFn(firstInput.setInputFiles)) {
        await firstInput.setInputFiles(videoPath);
        await delay(900);
        return true;
      }
    } catch {
      // continue
    }
    return false;
  };

  if (await trySetInputFiles()) return;

  const pickerPromise = hasFn(play.waitForEvent)
    ? play.waitForEvent("filechooser", { timeout: 30000 }).catch(() => null)
    : Promise.resolve(null);

  const clickUploadButton = async () => {
    if (hasFn(play.getByRole)) {
      try {
        const exactButton = play.getByRole("button", { name: "動画を選択", exact: true });
        const exactVisible = await exactButton.isVisible({ timeout: 1200 }).catch(() => false);
        if (exactVisible) {
          await exactButton.click({ force: true }).catch(() => {});
          return true;
        }
      } catch {
        // continue
      }

      try {
        const looseButton = play.getByRole("button", { name: /動画を選択/ });
        const looseVisible = await looseButton.isVisible({ timeout: 1200 }).catch(() => false);
        if (looseVisible) {
          await looseButton.click({ force: true }).catch(() => {});
          return true;
        }
      } catch {
        // continue
      }
    }

    if (hasFn(play.getByText)) {
      try {
        const textButton = play.getByText("動画を選択", { exact: true });
        const textVisible = await textButton.isVisible({ timeout: 1200 }).catch(() => false);
        if (textVisible) {
          await textButton.click({ force: true }).catch(() => {});
          return true;
        }
      } catch {
        // continue
      }
    }

    try {
      const point = await findTextPoint(tab, "動画を選択");
      if (point) {
        await tab.cua.click(point);
        return true;
      }
    } catch {
      // continue
    }

    return false;
  };

  const clickedUploadButton = await clickUploadButton();
  if (!clickedUploadButton) {
    const controlSelectors = [
      'button[aria-label="動画を選択"]',
      '[data-e2e="select_video_button"]',
    ];
    for (const selector of controlSelectors) {
      if (hasFn(play.locator)) {
        try {
          const node = play.locator(selector).first();
          const visible = await node.isVisible().catch(() => false);
          if (visible) {
            await node.click({ force: true }).catch(() => {});
            break;
          }
        } catch {
          // continue
        }
      }
      const point = await findTextPoint(tab, selector);
      if (point) {
        await tab.cua.click(point);
        break;
      }
    }
  }

  if (await trySetInputFiles()) {
    return;
  }

  const chooser = pickerPromise ? await pickerPromise : null;
  if (!chooser) {
    throw new Error(`${shortId}: file chooser method unavailable in this runtime`);
  }

  const hasSetFiles = chooser && hasFn(chooser.setFiles);
  if (!hasSetFiles) {
    throw new Error(`${shortId}: file chooser returned but cannot set files`);
  }

  await chooser.setFiles(videoPath);
  if (inputCount === 0) {
    await delay(800);
  await play.evaluate(() => {
      const fileInputs = [...document.querySelectorAll("input[type='file']")];
      if (!fileInputs.length) return;
      fileInputs[0].dispatchEvent(new MouseEvent("click", { bubbles: true }));
    });
  }
  await delay(1700);
}

function getDateStringForLog(value) {
  const m = String(value || "").match(/(\d{1,2})/);
  if (!m) return "";
  return String(m[1]).padStart(2, "0");
}

export async function openUploadTab(browser) {
  const tab = await browser.tabs.new();
  try {
    await tab.goto("https://www.tiktok.com/tiktokstudio/upload", {
      waitUntil: "domcontentloaded",
      timeoutMs: 90000,
    });
  } catch (error) {
    const currentUrl = await tab.url().catch(() => "");
    if (!currentUrl || !currentUrl.includes("tiktokstudio/upload")) {
      throw error;
    }
  }
  await waitForUploadControl(tab).catch(async (error) => {
    const snapshot = await tab.playwright.domSnapshot().catch(() => "");
    if (snapshot.includes("ログイン") || snapshot.includes("Log in")) {
      throw new Error("ログインが必要です: TikTokStudioに再ログインしてください");
    }
    throw error;
  });

  let snapshot = "";
  for (let attempt = 0; attempt < 20; attempt += 1) {
    snapshot = await tab.playwright.domSnapshot();
    if (
      snapshot.includes("動画を選択") ||
      snapshot.includes("動画を選択する") ||
      snapshot.includes("投稿予約する")
    ) {
      return tab;
    }
    await delay(700);
  }
  throw new Error("TikTok upload control did not render");
}

export async function uploadAndPrepare(tab, { shortId, videoPath, caption }) {
  await setFileForUpload(tab, videoPath, shortId);
  await setCaption(tab, caption);

  let prepared = false;
  for (let attempt = 0; attempt < 60; attempt += 1) {
    const snapshot = await tab.playwright.domSnapshot();
    const copyrightOk =
      snapshot.includes("問題は見つかりませんでした") || snapshot.includes("問題は見つかりませんでした。");
    const contentOk =
      snapshot.includes("違反は見つかりませんでした") || snapshot.includes("違反は見つかりませんでした。");
    if (snapshot.includes("アップロード完了") && copyrightOk && contentOk) {
      prepared = true;
      break;
    }
    await delay(3000);
  }
  if (!prepared) {
    throw new Error(`${shortId}: upload or content checks timed out`);
  }

  const coverPoint = await findTextPoint(tab, "カバーを編集");
  if (!coverPoint) throw new Error(`${shortId}: cover control not found`);
  await tab.cua.click(coverPoint);
  await delay(700);
  let snapshot = await tab.playwright.domSnapshot();
  if (!snapshot.includes("プロフィール内のプレビュー（4:3）")) {
    await tab.cua.click(coverPoint).catch(() => {});
    await delay(700);
    snapshot = await tab.playwright.domSnapshot();
  }
  if (!snapshot.includes("プロフィール内のプレビュー（4:3）")) {
    throw new Error(`${shortId}: cover editor did not open`);
  }

  const savePoint = await findTextPoint(tab, "保存");
  if (!savePoint) {
    throw new Error(`${shortId}: cover save control not found`);
  }
  await tab.cua.click(savePoint);
  await delay(1000);
  snapshot = await tab.playwright.domSnapshot();
  if (snapshot.includes("プロフィール内のプレビュー（4:3）")) {
    throw new Error(`${shortId}: cover did not save`);
  }

  if (snapshot.includes("さらに表示")) {
    await clickText(tab, "さらに表示").catch(() => {});
    await delay(350);
  }
  await clickText(tab, "投稿予約する", { timeoutMs: 9000 }).catch(async () => {
    await clickText(tab, "投稿予定", { timeoutMs: 8000 }).catch(() => {});
  });
  await delay(350);
}

export async function schedulePrepared(tab, { day, targetHour, caption = "" }) {
  const play = tab.playwright;
  const textboxes = hasFn(play.getByRole) ? play.getByRole("textbox") : null;
  const textboxCount = hasFn(textboxes?.count) ? await textboxes.count().catch(() => 0) : 0;
  let date = null;
  let time = null;
  let usedTextboxes = false;

  if (textboxCount >= 3) {
    await textboxes.nth(2).click().catch(() => {});
    await delay(250);
    const daySet = await play.evaluate((targetDay) => {
      const days = [...document.querySelectorAll(".day.valid")];
      const dayTexts = days.map((node) => (node.textContent || "").trim());
      const target = days.find((node) => getCleanText(node) === String(targetDay));
      if (!target) return false;
      target.click();
      return true;

      function getCleanText(node) {
        return (node.textContent || "").trim();
      }
    }, String(day));
    if (!daySet) throw new Error(`calendar day ${day} is unavailable`);

    const hourSet = await play.evaluate((targetHour) => {
      const candidates = [...document.querySelectorAll("input, [type='time'], [aria-label]")];
      const hours = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"];
      const target = candidates.find((element) => {
        const id = (element.id || "").toLowerCase();
        const name = (element.getAttribute("aria-label") || "").toLowerCase();
        const placeholder = (element.placeholder || "").toLowerCase();
        return placeholder.includes("時") || placeholder.includes("time") || name.includes("time") || name.includes("時") || id.includes("time");
      });
      if (!target) return null;
      target.focus();
      target.value = `${targetHour}:00`;
      target.dispatchEvent(new Event("input", { bubbles: true }));
      target.dispatchEvent(new Event("change", { bubbles: true }));
      return true;
    }, String(targetHour).padStart(2, "0"));
    if (!hourSet) {
      for (let i = 0; i < 8; i += 1) {
        const currentValue = await textboxes.nth(1).getAttribute("value");
        const currentHour = Number.parseInt((currentValue || "00").slice(0, 2), 10);
        if (currentHour === targetHour) break;
        const delta = Math.sign(targetHour - currentHour) * 520;
        const point = await textboxes.nth(1).evaluate((element) => {
          const rect = element.getBoundingClientRect();
          return { x: rect.x + 48, y: rect.y - 123 };
        });
        try {
          await tab.cua.scroll({ x: point.x, y: point.y, scrollX: 0, scrollY: delta });
        } catch {
          // ignore
        }
        await delay(450);
      }
    }

    time = await textboxes.nth(1).getAttribute("value").catch(() => null);
    usedTextboxes = true;
  } else {
    await clickText(tab, "投稿予約する").catch(() => {});
    const manual = await play.evaluate((targetDay, targetHourText) => {
      const dayInputs = [...document.querySelectorAll("input")].filter((input) => {
        const placeholder = (input.placeholder || "").trim();
        const label = (input.getAttribute("aria-label") || "").trim();
        return placeholder.includes("日") || label.includes("日");
      });
      const timeInputs = [...document.querySelectorAll("input")].filter((input) => {
        const placeholder = (input.placeholder || "").trim();
        const label = (input.getAttribute("aria-label") || "").trim();
        return placeholder.includes("時") || placeholder.includes("時間") || label.includes("時間") || input.type === "time";
      });
      if (dayInputs[0]) {
        dayInputs[0].value = targetDay;
        dayInputs[0].dispatchEvent(new Event("input", { bubbles: true }));
        dayInputs[0].dispatchEvent(new Event("change", { bubbles: true }));
      }
      if (timeInputs[0]) {
        timeInputs[0].value = `${targetHourText}:00`;
        timeInputs[0].dispatchEvent(new Event("input", { bubbles: true }));
        timeInputs[0].dispatchEvent(new Event("change", { bubbles: true }));
      }
      return {
        hasDay: Boolean(dayInputs[0]),
        hasTime: Boolean(timeInputs[0]),
      };
    }, getDateStringForLog(day), String(targetHour).padStart(2, "0"));

    date = new Date().toISOString().slice(0, 10);
    time = `${String(targetHour).padStart(2, "0")}:00`;
    usedTextboxes = manual?.hasTime || false;
  }

  let snapshot = await play.domSnapshot();
  const wantAiOn = snapshot.includes("AI生成コンテンツ\n- switch [checked]") || snapshot.includes("AI生成コンテンツを有効");
  if (!wantAiOn) {
    const aiPoint = await play.evaluate(() => {
      const elements = [...document.querySelectorAll("[role='switch'], [role='checkbox']")];
      const ai = elements.find((element) => (trimmedText(element) || "").includes("AI生成コンテンツ"));
      if (!ai) return null;
      const rect = ai.getBoundingClientRect();
      return { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };

      function trimmedText(node) {
        return (node?.innerText || node?.textContent || "").trim();
      }
    });
    if (aiPoint) {
      await tab.cua.click(aiPoint);
      await delay(450);
      snapshot = await play.domSnapshot();
    }
  }
  if (!snapshot.includes("AI生成コンテンツ")) {
    throw new Error("AI generated content label is off");
  }
  if (
    !snapshot.includes("問題は見つかりませんでした。") &&
    !snapshot.includes("問題は見つかりませんでした")
  ) {
    throw new Error("content checks are not both passing");
  }
  if (
    !snapshot.includes("違反は見つかりませんでした。") &&
    !snapshot.includes("違反は見つかりませんでした")
  ) {
    throw new Error("content checks are not both passing");
  }

  if (!date && textboxCount >= 3) {
    const rawDate = await textboxes.nth(2).getAttribute("value");
    date = rawDate || new Date().toISOString().slice(0, 10);
  }
  if (usedTextboxes && hasFn(textboxes.nth)) {
    const scheduledValue = await textboxes.nth(1).getAttribute("value").catch(() => null);
    if (scheduledValue) {
      time = scheduledValue.includes(":") ? scheduledValue : `${scheduledValue}:00`;
    }
  }

  await clickText(tab, "投稿予約する").catch(async () => {
    const radioFallback = hasFn(play.getByRole)
      ? play.getByRole("button", { name: "投稿予約する", exact: true })
      : null;
    await clickWhenAvailable(radioFallback, { timeoutMs: 4000, force: true }).catch(() => {});
  });
  await delay(5500);

  if (play.waitForURL && (await tab.url().catch(() => ""))?.includes("/tiktokstudio/upload")) {
    for (let i = 0; i < 10; i += 1) {
      await delay(1500);
      const current = await tab.url().catch(() => "");
      if (current.includes("/tiktokstudio/content")) break;
    }
  }
  const currentUrl = await tab.url().catch(() => "");
  if (!currentUrl.includes("/tiktokstudio/content")) {
    throw new Error("schedule submit did not reach the content list");
  }

  const row = await play.evaluate((expectedCaption) => {
    const prefix = expectedCaption.trim().slice(0, 64);
    const links = [...document.querySelectorAll('a[href*="/video/"]')];
    const direct = links.find((candidate) => (candidate.textContent || "").trim().startsWith(prefix));
    const link = direct || links.find((candidate) => {
      const txt = (candidate.textContent || "").trim();
      return txt && txt.includes(prefix);
    });
    if (!link) return null;
    let container = link;
    for (let level = 0; level < 6 && container.parentElement; level += 1) {
      container = container.parentElement;
    }
    return {
      url: link.href,
      text: (link.innerText || link.textContent || "").trim(),
      displayedSchedule: (container.innerText || container.textContent || "").trim(),
    };
  }, caption);
  if (!row) throw new Error("scheduled post receipt not found");

  return {
    date,
    time,
    caption,
    url: row.url,
    rowText: row.text,
    displayedSchedule: row.displayedSchedule,
    coverSaved: true,
  };
}
