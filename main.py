import streamlit as st
import json
import random
import time
import os
import uuid
from pathlib import Path
import urllib.parse


def load_countries():
    """国名データを読み込む"""
    # スクリプトファイルのディレクトリを基準とした絶対パス
    script_dir = os.path.dirname(os.path.abspath(__file__))
    countries_path = os.path.join(script_dir, 'countries.json')
    
    try:
        with open(countries_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"countries.jsonファイルが見つかりません: {countries_path}")
        st.info("dataフォルダとcountries.jsonファイルが存在することを確認してください。")
        return []
    except json.JSONDecodeError:
        st.error("countries.jsonファイルの形式が正しくありません。")
        return []


def get_random_options(countries, correct_answer, num_options=4):
    """正解を含む選択肢を生成する"""
    options = [correct_answer]
    other_countries = [c['name'] for c in countries if c['name'] != correct_answer]
    options.extend(random.sample(other_countries, num_options - 1))
    random.shuffle(options)
    return options


def show_flag_image(country):
    """国旗画像を表示（API経由、フォールバック付き）"""
    if 'code' in country:
        # 複数のAPIを順番に試行
        flag_urls = [
            f"https://flagcdn.com/w320/{country['code'].lower()}.png",
            f"https://flagsapi.com/{country['code'].upper()}/flat/256.png",
            f"https://countryflagsapi.netlify.app/flag/{country['code'].lower()}.svg"
        ]
        
        image_displayed = False
        
        for i, flag_url in enumerate(flag_urls):
            try:
                st.image(flag_url, width=300)
                if i > 0:  # 最初のAPI以外を使用した場合
                    st.caption(f"🌐 API {i+1}から取得")
                image_displayed = True
                break
            except Exception:
                continue
        
        # 全てのAPIが失敗した場合、ローカルファイルにフォールバック
        if not image_displayed:
            flag_path = f"data/flags/{country['flag']}"
            if os.path.exists(flag_path):
                st.image(flag_path, width=300)
                st.caption("⚠️ ローカル画像を表示中")
            else:
                st.error(f"国旗画像を取得できません: {country['name']}")
                st.info("ネットワーク接続とローカルファイルを確認してください")
    else:
        st.error(f"国コードが見つかりません: {country['name']}")


def main():
    st.set_page_config(page_title="国旗クイズ", page_icon="🏳️", layout="centered")

    st.header("🏳️ 国旗クイズ")

    # セッション状態の初期化
    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'menu'
    if 'countries' not in st.session_state:
        st.session_state.countries = load_countries()
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'current_options' not in st.session_state:  # 追加：現在の選択肢を保存
        st.session_state.current_options = []
    if 'selected_answer' not in st.session_state:
        st.session_state.selected_answer = None
    if 'show_result' not in st.session_state:
        st.session_state.show_result = False
    if 'answers_history' not in st.session_state:  # 追加：回答履歴を保存
        st.session_state.answers_history = []
    if 'question_start_time' not in st.session_state:  # 追加：問題開始時刻
        st.session_state.question_start_time = None

    # メニュー画面
    if st.session_state.game_state == 'menu':
        # show_sidebar()

        st.markdown("🎯 国旗を見て、正しい国名を4つの選択肢から選んでください")
        st.info("問題数を選択してください")

        if st.button("10問", use_container_width=True):
            start_game(10)

        if st.button("30問", use_container_width=True):
            start_game(30)

        if st.button("100問", use_container_width=True):
            start_game(100)

        if st.button("すべての国", use_container_width=True):
            start_game(len(st.session_state.countries))


    # ゲーム画面
    elif st.session_state.game_state == 'playing':
        show_game()

    # 結果画面
    elif st.session_state.game_state == 'result':
        # show_sidebar()
        show_results()


def start_game(num_questions):
    """ゲームを開始する"""
    st.session_state.game_state = 'playing'
    st.session_state.current_question = 0
    st.session_state.correct_answers = 0
    st.session_state.start_time = time.time()
    st.session_state.selected_answer = None
    st.session_state.show_result = False
    st.session_state.answers_history = []

    # 問題をランダムに選択
    selected_countries = random.sample(st.session_state.countries, num_questions)
    st.session_state.questions = selected_countries

    # 最初の問題の選択肢を生成
    generate_options_for_current_question()

    # 最初の問題の開始時刻を記録
    st.session_state.question_start_time = time.time()

    st.rerun()


def generate_options_for_current_question():
    """現在の問題の選択肢を生成"""
    if st.session_state.current_question < len(st.session_state.questions):
        current_country = st.session_state.questions[st.session_state.current_question]
        st.session_state.current_options = get_random_options(
            st.session_state.countries,
            current_country['name']
        )
        # 問題開始時刻を記録
        st.session_state.question_start_time = time.time()


def show_game():
    """ゲーム画面を表示"""
    if st.session_state.current_question >= len(st.session_state.questions):
        st.session_state.game_state = 'result'
        st.rerun()
        return

    current_country = st.session_state.questions[st.session_state.current_question]

    # 進捗表示
    progress = (st.session_state.current_question + 1) / len(st.session_state.questions)
    st.progress(progress)

    st.subheader(f"問題 {st.session_state.current_question + 1} / {len(st.session_state.questions)}")

    colA, colB= st.columns(2)

    # 国旗表示
    with colA:
        show_flag_image(current_country)

    # 選択肢表示または結果表示
    if not st.session_state.show_result:

        # 選択肢ボタン
        with colB:
            for i, option in enumerate(st.session_state.current_options):


                button_key = f"option_{st.session_state.current_question}_{i}"

                if st.button(option, key=button_key, use_container_width=True):
                    # 回答時間を計算
                    answer_time = time.time() - st.session_state.question_start_time

                    # 正解・不正解の判定
                    is_correct = option == current_country['name']
                    if is_correct:
                        st.session_state.correct_answers += 1

                    # 回答履歴に追加
                    st.session_state.answers_history.append({
                        'question': current_country['name'],
                        'selected': option,
                        'correct': is_correct,
                        'answer_time': answer_time
                    })

                    st.session_state.selected_answer = option
                    st.session_state.show_result = True
                    st.rerun()


    # サイドメニュー
    # show_sidebar()

    # 結果表示
    if st.session_state.show_result:

        # 回答時間を表示
        if st.session_state.answers_history:
            last_answer = st.session_state.answers_history[-1]
            answer_time = last_answer['answer_time']
            with colB:
                st.info(f"⏱️ 回答時間: {answer_time:.1f}秒")

        if st.session_state.selected_answer == current_country['name']:
            with colB:
                st.success(f"✅ 正解！ {current_country['name']} です")
        else:
            with colB:
                st.error(f"❌ 不正解... 正解は {current_country['name']} でした")
                st.info(f"あなたの答え: {st.session_state.selected_answer}")

        # 次の問題に進む
        with colB:
            if st.button("次の問題へ", key="next_question", use_container_width=True):
                move_to_next_question()


        # ホームボタン
        st.write('')
        st.write('')
        st.write('')

        if st.button("🏠 ホームに戻る", use_container_width=True):
            st.session_state.game_state = 'menu'
            st.rerun()


def move_to_next_question():
    """次の問題に移動"""
    st.session_state.current_question += 1
    st.session_state.selected_answer = None
    st.session_state.show_result = False

    # 次の問題の選択肢を生成
    generate_options_for_current_question()

    st.rerun()


def show_results():
    """結果画面を表示"""
    end_time = time.time()
    total_time = end_time - st.session_state.start_time

    st.header("🎉 クイズ終了！")

    # 結果統計
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("問題数", len(st.session_state.questions))

    with col2:
        st.metric("正答数", st.session_state.correct_answers)

    with col3:
        accuracy = (st.session_state.correct_answers / len(st.session_state.questions)) * 100
        st.metric("正答率", f"{accuracy:.1f}%")

    # 時間統計
    col4, col5, col6 = st.columns(3)

    with col4:
        minutes = int(total_time // 60)
        seconds = int(total_time % 60)
        st.metric("総所要時間", f"{minutes}分{seconds}秒")

    with col5:
        if st.session_state.answers_history:
            avg_time = sum(answer['answer_time'] for answer in st.session_state.answers_history) / len(
                st.session_state.answers_history)
            st.metric("平均回答時間", f"{avg_time:.1f}秒")

    with col6:
        if st.session_state.answers_history:
            fastest_time = min(answer['answer_time'] for answer in st.session_state.answers_history)
            st.metric("最速回答時間", f"{fastest_time:.1f}秒")

    # 評価メッセージ
    if accuracy >= 90:
        st.success("🏆 素晴らしい！国旗博士ですね！")
    elif accuracy >= 70:
        st.info("👍 良い成績です！")
    elif accuracy >= 50:
        st.warning("📖 もう少し頑張りましょう！")
    else:
        st.error("📚 国旗の勉強をもっとしてみましょう！")

    # 詳細結果
    with st.expander("詳細結果を見る", expanded=False):
        for i, answer in enumerate(st.session_state.answers_history):
            status = "✅" if answer['correct'] else "❌"
            time_str = f"{answer['answer_time']:.1f}秒"
            st.write(f"{i + 1}. {answer['question']} - {status} ({answer['selected']}) - {time_str}")

    # SNSシェアセクションを呼び出し
    create_sns_share_section(
        accuracy=accuracy,
        correct_answers=st.session_state.correct_answers,
        total_questions=len(st.session_state.questions),
        minutes=minutes,
        seconds=seconds
    )

    # ホームに戻る
    if st.button("ホームに戻る", use_container_width=True):
        st.session_state.game_state = 'menu'
        st.rerun()


def create_sns_share_section(accuracy, correct_answers, total_questions, minutes, seconds):
    """SNSシェアセクションを作成"""

    st.subheader("📱 結果をシェア")

    # シェア用テキスト作成
    share_text = f"""🏴‍☠️ 国旗クイズの結果 🏴‍☠️

正答率: {accuracy:.1f}%
正答数: {correct_answers}/{total_questions}
総所要時間: {minutes}分{seconds}秒
"""

    # 評価に応じたハッシュタグ
    if accuracy >= 90:
        share_text += "\n#国旗博士 #完璧 #国旗クイズ"
    elif accuracy >= 70:
        share_text += "\n#国旗上級者 #国旗クイズ"
    elif accuracy >= 50:
        share_text += "\n#国旗勉強中 #国旗クイズ"
    else:
        share_text += "\n#国旗初心者 #国旗クイズ #がんばろう"

    # Font Awesome CDN読み込み
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """, unsafe_allow_html=True)

    # CSS for social buttons with official icons
    st.markdown("""
    <style>
    .social-button {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-decoration: none;
        padding: 15px;
        border-radius: 10px;
        transition: transform 0.2s, box-shadow 0.2s;
        color: white;
        font-weight: bold;
        font-size: 14px;
        width: 100%;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .social-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        text-decoration: none;
        color: white;
    }

    .line-button {
        background: linear-gradient(135deg, #06C755 0%, #04B84F 100%);
    }

    .x-button {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
    }

    .social-icon {
        font-size: 28px;
        margin-bottom: 8px;
    }

    .social-text {
        font-size: 16px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    # URLエンコード処理
    try:
        encoded_text = urllib.parse.quote(share_text)
    except Exception as e:
        st.error("テキストのエンコードに失敗しました")
        return

    # シェアボタン
    col_line, col_x = st.columns(2, gap="medium")

    with col_line:
        line_url = f"https://social-plugins.line.me/lineit/share?text={encoded_text}"
        st.markdown(f'''
        <div style="text-align: center;">
            <a href="{line_url}" target="_blank" class="social-button line-button" aria-label="LINEでシェア">
                <div class="social-icon">
                    <i class="fab fa-line"></i>
                </div>
                <div class="social-text">LINE</div>
            </a>
        </div>
        ''', unsafe_allow_html=True)

    with col_x:
        x_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
        st.markdown(f'''
        <div style="text-align: center;">
            <a href="{x_url}" target="_blank" class="social-button x-button" aria-label="Xでシェア">
                <div class="social-icon">
                    <i class="fab fa-x-twitter"></i>
                </div>
                <div class="social-text">X (Twitter)</div>
            </a>
        </div>
        ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()