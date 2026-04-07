"""事務さん向け: 募集要項PDF URL登録・確認画面

Streamlit Cloud にデプロイ。Claude APIは使わない。
データは session_state で管理し、JSONダウンロードで船登さんに渡す。
"""
import json
from pathlib import Path

import streamlit as st

# ─── パス設定 ──────────────────────────────────
APP_DIR = Path(__file__).parent
MASTER_PATH = APP_DIR / "universities.json"
INITIAL_REVIEW_PATH = APP_DIR / "pdf_review.json"

TYPE_LABELS = {"national": "国立", "public": "公立", "private": "私立"}
TYPE_ORDER = {"national": 0, "public": 1, "private": 2}

EXAM_TYPE_OPTIONS = ["一般選抜", "学校推薦型選抜", "総合型選抜", "入試ガイド", "その他"]

# ─── カスタムCSS ──────────────────────────────
CUSTOM_CSS = """
<style>
    .stApp { background-color: #fafafa; color: #333; }
    [data-testid="stSidebar"] { display: none; }

    h1 { color: #2c3e50 !important; font-weight: 600 !important;
         border-bottom: 2px solid #5b7a9d; padding-bottom: 12px !important; }
    h2 { color: #2c3e50 !important; font-weight: 500 !important; }
    h3 { color: #4a6785 !important; font-weight: 500 !important; }

    .stProgress > div > div > div { background-color: #5b7a9d !important; }
    .stProgress > div > div { background-color: #e0e0e0 !important; }

    .stButton > button { border-radius: 6px; font-weight: 500; }
    .stButton > button[kind="primary"],
    .stButton > button[kind="primary"] span,
    .stButton > button[kind="primary"] p {
        background-color: #5b7a9d !important; border-color: #5b7a9d !important;
        color: #fff !important; }
    .stButton > button[kind="primary"]:hover {
        background-color: #4a6785 !important; border-color: #4a6785 !important; }

    /* ファイルアップローダーのボタン */
    [data-testid="stFileUploader"] button,
    [data-testid="stFileUploader"] button span,
    [data-testid="stFileUploader"] button p {
        color: #fff !important; }

    [data-testid="stExpander"] {
        border: 1px solid #e0e0e0 !important; border-radius: 8px !important;
        margin-bottom: 4px !important; background-color: #fff !important; }
    [data-testid="stExpander"] summary { font-weight: 500 !important; }

    .stTextInput > div > div > input { border-radius: 6px !important; }

    /* 強制ライトモード */
    .stApp, .stApp * { color-scheme: light !important; }
    [data-testid="stHeader"] { background-color: #fafafa !important; }

    .stSelectbox > div > div,
    .stTextInput > div > div,
    .stNumberInput > div > div {
        background-color: #fff !important; color: #333 !important; }
    .stSelectbox > div > div > div,
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #fff !important; color: #333 !important; }
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] div { color: #333 !important; }
    .stTextInput input, .stNumberInput input {
        background-color: #fff !important; color: #333 !important; }
    input::placeholder { color: #999 !important; }

    [data-testid="stMetric"] { background-color: #fff !important; }
    [data-testid="stMetricValue"] { color: #2c3e50 !important; }
    [data-testid="stMetricLabel"] { color: #666 !important; }

    .stRadio label span { color: #333 !important; }
    .stRadio [role="radiogroup"] label { color: #333 !important; }

    [data-testid="stExpander"] p,
    [data-testid="stExpander"] span,
    [data-testid="stExpander"] label,
    [data-testid="stExpander"] div { color: #333 !important; }
    [data-testid="stExpander"] a { color: #5b7a9d !important; }
    [data-testid="stExpander"] .stCaption,
    [data-testid="stExpander"] .stCaption * { color: #888 !important; }

    [data-baseweb="popover"], [data-baseweb="menu"],
    ul[role="listbox"], ul[role="listbox"] li {
        background-color: #fff !important; color: #333 !important; }
    ul[role="listbox"] li:hover { background-color: #f0f4f8 !important; }

    hr { border-color: #e8e8e8 !important; }

    .guide-box {
        background: #f0f4f8; border-left: 4px solid #5b7a9d;
        padding: 16px 20px; border-radius: 0 8px 8px 0; margin-bottom: 20px;
        color: #2c3e50; line-height: 1.8;
    }
    .guide-box ol { margin: 8px 0 0 0; padding-left: 20px; }
    .guide-box li { margin-bottom: 4px; }

    .download-box {
        background: #eef4ee; border: 2px solid #5b7a9d;
        padding: 16px 20px; border-radius: 8px; margin: 16px 0;
        color: #2c3e50;
    }
</style>
"""


def load_master() -> dict:
    with open(MASTER_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return {u["id"]: u for u in data["universities"]}


def init_review() -> dict:
    """初期データを生成する。リポに同梱の pdf_review.json があればそれを使う。"""
    if INITIAL_REVIEW_PATH.exists():
        with open(INITIAL_REVIEW_PATH, encoding="utf-8") as f:
            return json.load(f)
    master = load_master()
    review = {}
    for uid, uni in master.items():
        review[uid] = {
            "name": uni["name"],
            "name_full": uni.get("name_full", f"{uni['name']}医学部医学科"),
            "type": uni["type"],
            "admission_url": uni.get("admission_url", ""),
            "exam_types": uni.get("exam_types", []),
            "pdfs": [],
            "status": "未確認",
            "notes": "",
        }
    return review


def main():
    st.set_page_config(
        page_title="募集要項 PDF URL登録",
        layout="wide",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # session_state でデータ管理（Streamlit Cloudではファイル書き込み不可）
    if "review" not in st.session_state:
        st.session_state.review = init_review()

    review = st.session_state.review

    # ─── ヘッダー ─────────────────────────────
    st.title("医学部 募集要項 PDF URL 登録")

    # ─── 前回データの読み込み ──────────────────
    if not st.session_state.get("data_loaded"):
        st.markdown("""
<div class="guide-box">
<strong>前回の続きから作業する場合</strong><br>
前回ダウンロードした <code>pdf_review.json</code> をアップロードしてください。<br>
初めての場合はそのまま下へスクロールしてください。
</div>
        """, unsafe_allow_html=True)

        resume_file = st.file_uploader(
            "前回の登録データを読み込む（pdf_review.json）",
            type=["json"],
            key="resume_upload",
        )
        if resume_file:
            try:
                imported = json.loads(resume_file.read().decode("utf-8"))
                sample_key = next(iter(imported))
                if "name" in imported[sample_key]:
                    st.session_state.review = imported
                    st.session_state.data_loaded = True
                    review = imported
                    n = sum(1 for v in imported.values() if v["status"] == "確認済み")
                    st.success(f"読み込み完了 -- {n}校が確認済みの状態で復元されました")
                    st.rerun()
                else:
                    st.error("ファイル形式が正しくありません")
            except Exception as e:
                st.error(f"読み込みエラー: {e}")

        st.divider()

    st.markdown("""
<div class="guide-box">
<strong>やること</strong>
<ol>
<li>下のリストから大学名をクリックして開く</li>
<li>「入試情報ページを開く」リンクから、その大学のサイトに移動する</li>
<li>サイト上で募集要項のPDFを見つけたら、PDFのリンクを右クリック →「リンクのアドレスをコピー」</li>
<li>この画面に戻り、選抜種別（一般選抜 / 推薦 / 総合型）を選んで、URL欄に貼り付け →「追加」ボタン</li>
<li>その大学の登録が全部終わったら、ステータスを「確認済み」に変更する</li>
<li><strong>作業の区切りごとに「登録データをダウンロード」を押して、ファイルを保存してください（タブを閉じると消えます）</strong></li>
</ol>
</div>
    """, unsafe_allow_html=True)

    # ─── データダウンロード（上部） ──────────
    total = len(review)
    confirmed = sum(1 for v in review.values() if v["status"] == "確認済み")
    unchecked = total - confirmed

    if confirmed > 0:
        st.markdown('<div class="download-box">', unsafe_allow_html=True)
        dl_col1, dl_col2 = st.columns([3, 1])
        with dl_col1:
            st.markdown(f"**{confirmed}校 / {total}校** の登録が完了しています。  \n"
                        f"ダウンロードして船登に送ってください。")
        with dl_col2:
            review_json = json.dumps(review, ensure_ascii=False, indent=2)
            st.download_button(
                label="登録データをダウンロード",
                data=review_json,
                file_name="pdf_review.json",
                mime="application/json",
                type="primary",
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # ─── フィルター ───────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_type = st.selectbox("種別で絞り込み", ["すべて", "国立", "公立", "私立"])
    with col2:
        filter_status = st.selectbox("ステータスで絞り込み", ["すべて", "未確認", "確認済み"])
    with col3:
        search_text = st.text_input("大学名で検索", "")

    # ─── 進捗 ─────────────────────────────────
    st.progress(confirmed / total if total > 0 else 0)
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("全大学", f"{total}校")
    col_b.metric("確認済み", f"{confirmed}校")
    col_c.metric("残り", f"{unchecked}校")

    st.divider()

    # ─── 大学一覧 ─────────────────────────────
    changed = False

    sorted_items = sorted(
        review.items(),
        key=lambda x: TYPE_ORDER.get(x[1]["type"], 9),
    )

    for uid, uni in sorted_items:
        type_label = TYPE_LABELS.get(uni["type"], "")
        if filter_type != "すべて" and type_label != filter_type:
            continue
        if filter_status != "すべて" and uni["status"] != filter_status:
            continue
        if search_text and search_text not in uni["name"]:
            continue

        status_mark = "[ OK ]" if uni["status"] == "確認済み" else "[    ]"
        pdf_count = len([p for p in uni.get("pdfs", []) if p.get("url")])
        badge = f" -- {pdf_count}件登録済み" if pdf_count > 0 else ""

        with st.expander(f"{status_mark}  {type_label} / {uni['name']}{badge}"):
            if uni.get("admission_url"):
                st.markdown(f"[入試情報ページを開く （{uni['name']}）]({uni['admission_url']})")
            else:
                st.caption("入試情報ページURLなし")

            if uni.get("exam_types"):
                st.caption(f"対象選抜: {' / '.join(uni['exam_types'])}")

            st.markdown("---")

            # ─── 登録済みPDF ──────────────────
            pdfs = uni.get("pdfs", [])

            if pdfs:
                st.markdown("**登録済みPDF**")
                for i, pdf in enumerate(pdfs):
                    pc1, pc2, pc3 = st.columns([2, 6, 1])
                    with pc1:
                        cur_type = pdf.get("exam_type", "その他")
                        idx = EXAM_TYPE_OPTIONS.index(cur_type) if cur_type in EXAM_TYPE_OPTIONS else 4
                        new_type = st.selectbox(
                            "種別", EXAM_TYPE_OPTIONS, index=idx,
                            key=f"type_{uid}_{i}", label_visibility="collapsed",
                        )
                        if new_type != cur_type:
                            pdf["exam_type"] = new_type
                            changed = True
                    with pc2:
                        new_url = st.text_input(
                            "URL", value=pdf.get("url", ""),
                            key=f"url_{uid}_{i}", label_visibility="collapsed",
                        )
                        if new_url != pdf.get("url", ""):
                            pdf["url"] = new_url
                            pdf["source"] = "manual"
                            pdf["confirmed"] = True
                            changed = True
                    with pc3:
                        if st.button("削除", key=f"del_{uid}_{i}"):
                            pdfs.pop(i)
                            changed = True
                            st.rerun()

            # ─── PDF追加 ──────────────────────
            st.markdown("**PDF追加** -- 選抜種別を選び、URLを貼り付けて「追加」を押してください")
            ac1, ac2, ac3 = st.columns([2, 6, 1])
            with ac1:
                add_type = st.selectbox(
                    "選抜種別", EXAM_TYPE_OPTIONS,
                    key=f"addtype_{uid}", label_visibility="collapsed",
                )
            with ac2:
                add_url = st.text_input(
                    "PDFのURL", key=f"addurl_{uid}",
                    placeholder="https://www.example.ac.jp/.../boshu.pdf",
                    label_visibility="collapsed",
                )
            with ac3:
                if st.button("追加", key=f"addbtn_{uid}", type="primary"):
                    if add_url.strip():
                        pdfs.append({
                            "exam_type": add_type,
                            "url": add_url.strip(),
                            "source": "manual",
                            "confirmed": True,
                        })
                        uni["pdfs"] = pdfs
                        changed = True
                        st.rerun()

            # ─── ステータス ────────────────────
            st.markdown("---")
            sc1, sc2 = st.columns([1, 3])
            with sc1:
                new_status = st.radio(
                    "ステータス",
                    ["未確認", "確認済み"],
                    index=0 if uni["status"] == "未確認" else 1,
                    key=f"status_{uid}", horizontal=True,
                )
                if new_status != uni["status"]:
                    uni["status"] = new_status
                    changed = True
            with sc2:
                new_notes = st.text_input(
                    "メモ（任意）", value=uni.get("notes", ""),
                    key=f"notes_{uid}",
                    placeholder="例: 推薦の要項はまだ公開されていない",
                )
                if new_notes != uni.get("notes", ""):
                    uni["notes"] = new_notes
                    changed = True

    # ─── 保存 ─────────────────────────────────
    if changed:
        st.session_state.review = review
        st.toast("保存しました")

    # ─── フッター: ダウンロード ────────────────
    st.divider()
    st.markdown("### 作業完了時")
    st.markdown("下のボタンからデータをダウンロードし、**船登に送ってください**。  \n"
                "途中の状態でもダウンロードできます。続きは後日でも大丈夫です。")

    review_json = json.dumps(review, ensure_ascii=False, indent=2)
    st.download_button(
        label="登録データをダウンロード",
        data=review_json,
        file_name="pdf_review.json",
        mime="application/json",
        type="primary",
        key="dl_footer",
    )


if __name__ == "__main__":
    main()
