import requests
import json
import os
from pathlib import Path
import time

def download_flag_image(country_code, filename, size="w320"):
    """
    flagcdn.com APIを使用して国旗画像をダウンロード
    size: w20, w40, w80, w160, w320, w640, w1280, w2560
    """
    url = f"https://flagcdn.com/{size}/{country_code.lower()}.png"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # data/flags フォルダに保存
        flag_path = Path("data/flags") / filename
        flag_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(flag_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
        return False

def get_country_codes():
    """
    ISO 3166-1 alpha-2 国コードマッピング
    """
    country_codes = {
        "日本": "jp",
        "アメリカ": "us",
        "中国": "cn",
        "韓国": "kr",
        "イギリス": "gb",
        "フランス": "fr",
        "ドイツ": "de",
        "イタリア": "it",
        "スペイン": "es",
        "オーストラリア": "au",
        "カナダ": "ca",
        "ブラジル": "br",
        "インド": "in",
        "ロシア": "ru",
        "メキシコ": "mx",
        "タイ": "th",
        "ベトナム": "vn",
        "インドネシア": "id",
        "フィリピン": "ph",
        "マレーシア": "my",
        "シンガポール": "sg",
        "トルコ": "tr",
        "エジプト": "eg",
        "南アフリカ": "za",
        "ナイジェリア": "ng",
        "アルゼンチン": "ar",
        "チリ": "cl",
        "ペルー": "pe",
        "コロンビア": "co",
        "ウルグアイ": "uy",
        "パラグアイ": "py",
        "ベネズエラ": "ve",
        "エクアドル": "ec",
        "ボリビア": "bo",
        "ガイアナ": "gy",
        "スリナム": "sr",
        "ノルウェー": "no",
        "スウェーデン": "se",
        "フィンランド": "fi",
        "デンマーク": "dk",
        "オランダ": "nl",
        "ベルギー": "be",
        "スイス": "ch",
        "オーストリア": "at",
        "ポーランド": "pl",
        "チェコ": "cz",
        "ハンガリー": "hu",
        "ルーマニア": "ro",
        "ブルガリア": "bg",
        "ギリシャ": "gr",
        "クロアチア": "hr",
        "セルビア": "rs",
        "スロベニア": "si",
        "スロバキア": "sk",
        "ポルトガル": "pt",
        "アイルランド": "ie",
        "アイスランド": "is",
        "リトアニア": "lt",
        "ラトビア": "lv",
        "エストニア": "ee",
        "ウクライナ": "ua",
        "ベラルーシ": "by",
        "モルドバ": "md",
        "ジョージア": "ge",
        "アルメニア": "am",
        "アゼルバイジャン": "az",
        "カザフスタン": "kz",
        "ウズベキスタン": "uz",
        "キルギス": "kg",
        "タジキスタン": "tj",
        "トルクメニスタン": "tm",
        "モンゴル": "mn",
        "北朝鮮": "kp",
        "ミャンマー": "mm",
        "ラオス": "la",
        "カンボジア": "kh",
        "ブルネイ": "bn",
        "東ティモール": "tl",
        "パプアニューギニア": "pg",
        "フィジー": "fj",
        "ニュージーランド": "nz",
        "バヌアツ": "vu",
        "ソロモン諸島": "sb",
        "サモア": "ws",
        "トンガ": "to",
        "ツバル": "tv",
        "ナウル": "nr",
        "キリバス": "ki",
        "マーシャル諸島": "mh",
        "ミクロネシア": "fm",
        "パラオ": "pw",
        "アフガニスタン": "af",
        "パキスタン": "pk",
        "バングラデシュ": "bd",
        "スリランカ": "lk",
        "ネパール": "np",
        "ブータン": "bt",
        "モルディブ": "mv",
        "イラン": "ir",
        "イラク": "iq",
        "シリア": "sy",
        "レバノン": "lb",
        "ヨルダン": "jo",
        "イスラエル": "il",
        "パレスチナ": "ps",
        "サウジアラビア": "sa",
        "イエメン": "ye",
        "オマーン": "om",
        "UAE": "ae",
        "カタール": "qa",
        "バーレーン": "bh",
        "クウェート": "kw",
        "アルジェリア": "dz",
        "モロッコ": "ma",
        "チュニジア": "tn",
        "リビア": "ly",
        "スーダン": "sd",
        "南スーダン": "ss",
        "エチオピア": "et",
        "エリトリア": "er",
        "ジブチ": "dj",
        "ソマリア": "so",
        "ケニア": "ke",
        "ウガンダ": "ug",
        "タンザニア": "tz",
        "ルワンダ": "rw",
        "ブルンジ": "bi",
        "マダガスカル": "mg",
        "モーリシャス": "mu",
        "セーシェル": "sc",
        "コモロ": "km",
        "モザンビーク": "mz",
        "ザンビア": "zm",
        "ジンバブエ": "zw",
        "ボツワナ": "bw",
        "ナミビア": "na",
        "レソト": "ls",
        "エスワティニ": "sz",
        "マラウイ": "mw",
        "アンゴラ": "ao",
        "ガボン": "ga",
        "赤道ギニア": "gq",
        "サントメ・プリンシペ": "st",
        "カメルーン": "cm",
        "中央アフリカ": "cf",
        "チャド": "td",
        "コンゴ共和国": "cg",
        "コンゴ民主共和国": "cd",
        "ニジェール": "ne",
        "マリ": "ml",
        "ブルキナファソ": "bf",
        "ガーナ": "gh",
        "コートジボワール": "ci",
        "リベリア": "lr",
        "シエラレオネ": "sl",
        "ギニア": "gn",
        "ギニアビサウ": "gw",
        "セネガル": "sn",
        "ガンビア": "gm",
        "カーボベルデ": "cv",
        "モーリタニア": "mr",
        "ベナン": "bj",
        "トーゴ": "tg"
    }
    return country_codes

def main():
    """メイン処理"""
    print("国旗画像ダウンロード開始...")
    
    # countries.jsonを読み込み
    with open('data/countries.json', 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    # 国コードマッピング取得
    country_codes = get_country_codes()
    
    # data/flags フォルダを作成
    Path("data/flags").mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    total_count = len(countries)
    
    for country in countries:
        country_name = country['name']
        filename = country['flag']
        
        if country_name in country_codes:
            country_code = country_codes[country_name]
            
            # 画像をダウンロード
            if download_flag_image(country_code, filename):
                success_count += 1
            
            # レート制限対策
            time.sleep(0.5)
        else:
            print(f"Country code not found for: {country_name}")
    
    print(f"\nダウンロード完了: {success_count}/{total_count} 件")
    print(f"保存先: data/flags/")

if __name__ == "__main__":
    main()