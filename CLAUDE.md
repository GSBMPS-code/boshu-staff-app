# boshu-staff-app

松濤舎スタッフ向け「医学部 募集要項 PDF URL 登録ツール」。
事務スタッフが募集要項PDFのURLを手作業で登録し、`pdf_review.json` をダウンロードして船登さんに渡す。

## 技術スタック

- Python 3.x / Streamlit / Streamlit Cloud
- データは JSON + `st.session_state` で管理。DBは使わない

## データモデル

- `universities.json`: 大学マスタ。`id`, `type`("national"|"public"|"private"), `exam_types`, `admission_url`
- `pdf_review.json`: 登録データ。キーは大学ID。`pdfs[]`（`exam_type`, `url`, `source`, `confirmed`）, `status`("未確認"|"確認済み"), `notes`

## 制約（重要）

- **Claude API は使わない。** 純粋なフロントエンドアプリとして維持する
- **DB・バックエンドを追加しない。** Streamlit Cloud ではサーバー側ファイル書き込み不可。データ永続化は JSON ダウンロード/アップロードのみ
- **サイドバーは非表示。** CSSで消しているので、`st.sidebar` は使わない
- **ブランドカラーは `#5b7a9d`。** UIを変更する場合はこの色に揃える
- **強制ライトモード。** ダークモード対応は不要
- **大学の表示順は種別順**（国立→公立→私立）。変えない

## コマンド

```bash
streamlit run app.py        # ローカル起動
pip install -r requirements.txt  # 依存インストール
```

## 対応言語

日本語で応答してください。コミットメッセージも日本語で構いません。
