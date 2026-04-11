# boshu-staff-app

松濤舎スタッフ向け「医学部 募集要項 PDF URL 登録ツール」。

## 概要

- 全国の医学部医学科の募集要項PDFのURLを、事務スタッフが手作業で登録・管理するためのWebアプリ
- 登録データは `pdf_review.json` としてダウンロードし、船登さんに渡す運用フロー
- Claude API は使わない（純粋なフロントエンドアプリ）

## 技術スタック

- **言語**: Python 3.x
- **フレームワーク**: Streamlit
- **デプロイ**: Streamlit Cloud
- **データ管理**: JSON ファイル + `st.session_state`（DB不使用）

## ファイル構成

```
app.py               # メインアプリ（単一ファイル）
universities.json    # 大学マスタデータ（id, name, type, admission_url, exam_types）
pdf_review.json      # 登録状況の初期データ / エクスポートデータ
requirements.txt     # 依存パッケージ（streamlit のみ）
```

## データモデル

### universities.json（マスタ）
- `id`: 大学識別子（例: "tokyo"）
- `type`: "national" | "public" | "private"
- `exam_types`: 対象の選抜種別リスト
- `admission_url`: 入試情報ページURL

### pdf_review.json（登録データ）
- キー: 大学ID
- `pdfs[]`: 登録済みPDFの配列（`exam_type`, `url`, `source`, `confirmed`）
- `status`: "未確認" | "確認済み"
- `notes`: メモ

## 開発時の注意

- Streamlit Cloud ではサーバー側ファイル書き込み不可。データ永続化は JSON ダウンロード/アップロードで行う
- UIは強制ライトモード。カスタムCSS（`CUSTOM_CSS`）でブランドカラー `#5b7a9d` を使用
- サイドバーは非表示に設定済み
- 大学は種別順（国立→公立→私立）でソート表示

## コマンド

```bash
# ローカル起動
streamlit run app.py

# 依存パッケージインストール
pip install -r requirements.txt
```

## 対応言語

日本語で応答してください。コミットメッセージも日本語で構いません。
