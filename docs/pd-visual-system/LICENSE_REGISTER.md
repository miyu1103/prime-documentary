# License Register

> コードライセンス、モデル重み、整列モデル、custom node、素材ライセンス、出力条件を別々に記録します。`unknown`を`approved`へ自動変換してはいけません。

| ID | Tool/model/asset | Artifact type | Version/hash | Source | License | Commercial use | Territory/output restrictions | Attribution | Decision | Reviewed at | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LIC-001 |  | code |  |  |  | unknown |  | unknown | review_required |  |  |

## Decision values

- `approved`
- `review_required`
- `rejected`
- `not_applicable`

## Hard gate

次のいずれかがある場合、本番利用を停止します。

- 非商用または用途制限
- 地域制限
- 出力物への制限
- 収益規模による追加契約
- モデルカードとLICENSEの矛盾
- third-party checkpoint/custom nodeの条件不明
- 出典URLまたは取得日時がない
