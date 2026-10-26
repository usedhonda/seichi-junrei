# 勝手に聖地巡礼 — seichi-junrei

**旅程を無理やり聖地巡礼にする、Codex限定Skill。旅の楽しさを数割アップ。**

すでに決まっている旅も、これから考える旅も。カレンダーやテキストから条件を整理し、旅程に合うアニメ・漫画・映画を探して、スポットと物語のつながりを調べます。そこから挿絵・地図・日ごとの旅程を組み合わせ、スマホで読める旅のしおりに仕上げます。

有名な名所だけでなく、作中の店や通り、背景の屋根や窓を探すのも楽しみ。現地で「この場面だ」と気づくための手がかりを、旅の順番で読める形にまとめます。

[公開サンプル](#3つの公開サンプル) · [使い方](#使い方) · [インストール](#インストール) · [利用範囲と権利](#利用範囲と権利)

## 3つの公開サンプル

作品ごとに、デザインと絵の演出を変えています。以下のリンクから実際に操作できます。

| 作品 × 行き先 | 旅の見どころ | 構成 |
| --- | --- | --- |
| [ジョジョ × エジプト](https://usedhonda.github.io/seichi-junrei/) | アスワンの街とアブ・シンベル。街の接写から砂漠の遠景、巨像へつなぐ冒険のしおり。イギーの小さな案内と、デフォルメの締めも | 2日・2目的地 |
| [コナン × シンガポール](https://usedhonda.github.io/seichi-junrei/conan/) | 朝のカヤトースト、ホーカーのランチ、ラッフルズのロング・バー。調査ノートの中に場面絵とキャラのスタンプを配置 | 1日・3目的地＋寄り道 |
| [MONSTER × ドイツ・チェコ](https://usedhonda.github.io/seichi-junrei/monster/) | ハイデルベルクの大学の窓、カウフボイレンのホテル、プラハのOPの街角。俯瞰の街、列車のホーム、肩越しの路地をたどるスリラーの旅 | 移動日込み5日・3目的地 |

個人の旅行日・便名・予約情報を含まないモデルルートです。挿絵はGPT Imageで制作した非公式ファンアートで、現地写真や公式の場面画像ではありません。

作中の舞台・ロケ地・モデルと、テーマを重ねて楽しむ場所は区別しています。ジョジョ版の遺跡をすべて作中の舞台と断定する構成ではありません。コナン版は本編全編との直接照合が未完了、MONSTER版は原作比較画像を目視した地点とアニメOPの訪問者報告を分けています。列車の接続・予約可能性などは、実際の訪問日に合わせた確認が必要です。

## 使い方

旅の決まり具合に合わせて始められます。たとえば、CodexでSkillを選んで次のように伝えます。

**予約がほぼ決まっている旅**

> この期間のカレンダーから旅行予定を読んで、空き時間を聖地巡礼にして。予約済みの飛行機とホテルはそのままで、旅仲間とスマホで読めるしおりがほしい。

**まだこれから考える旅**

> 来年の春、ドイツとチェコに5日くらい行きたい。漫画や映画の聖地を探して、作品とルートの候補から相談したい。ホテルは未定。

**一部だけ決まっている旅**

> シンガポールに2泊。飛行機は予約済み、ホテルはまだ。コナンを主役に、歩きすぎない行程を考えて。まずはルート案まで。

カレンダー接続は必須ではありません。テキストで日程・予約済みの内容・希望を渡しても使えます。カレンダーを読む場合は、接続とアクセス権が必要です。

まず、確定・仮決め・未定を分け、日程・同行者・移動条件・作品の好みなど、制作に影響する不足をまとめて確認します。今回は候補探し・ルート案・完成しおりのどこまで進めるかを合わせてから制作するため、すべて予約済みである必要はありません。詳しくは[旅程の事前整理](plugins/seichi-junrei/references/trip-intake.md)を参照してください。

## しおりができるまで

1. **旅を把握する。** 予約済みの便・ホテル、自由時間、予算や歩く量などの条件を整理します。確定した予定を勝手に動かしません。
2. **作品を選ぶ。** 行き先に関係するアニメ・漫画・映画を3〜5本、根拠付きで提案します。主役はユーザーが選び、すでに指定されていればその作品で進めます。「おまかせ」と明示された場合は選定も任せられます。
3. **場面と現地を調べる。** 話数・巻数・映画のシーン、場所を特定する手がかり、現在の訪問条件を確認します。検索記事の推測を確定情報に変えず、裏付けがない場所は聖地と断定しません。
4. **全体構成と絵コンテを決める。** 訪問順、本文、地図と一緒に、絵の枚数・役割・登場人物の動き・構図・テイストを設計します。
5. **絵としおりを制作する。** 作品に合う場面絵、案内役の小さなスタンプ、ときどき全員デフォルメの一枚絵などを使い分けます。同じ着席構図や同じサイズの絵を続けず、後半まで流れを作ります。
6. **スマホ向けHTMLを検証して渡す。** 地図・画像拡大・チェックリスト・保存などの操作と、実際の画面を確認します。

調査手順と制作計画の実例も同梱しています。

- [場面単位の聖地調査](plugins/seichi-junrei/references/scene-research.md) / [コナンの調査記録](plugins/seichi-junrei/examples/conan_singapore_research.md)
- 絵コンテ：[ジョジョ](plugins/seichi-junrei/examples/egypt_art_plan.md) / [コナン](plugins/seichi-junrei/examples/conan_singapore_art_plan.md) / [MONSTER](plugins/seichi-junrei/examples/monster_europe_art_plan.md)
- [モバイルしおりの制作手順](plugins/seichi-junrei/references/mobile-production.md)

## 完成するもの

標準成果物は、画像を内蔵した**単一HTMLファイル**です。公開URLやアカウントを作らず、旅仲間とファイルで共有できます。公開サイトを作るのは、ユーザーが明示的に希望した場合だけです。

表紙から旅の見取り図へ、そのまま日・場所の順に読み進めます。各スポットには、場面・見どころ・地図・次への移動をまとめ、都市間の移動日も旅の一章にします。地図や旅程だけを別ページへ切り離す構成にはしません。

保存したHTMLには本文・挿絵・地点・訪問順・チェック機能が残ります。**背景地図と外部の経路案内には通信が必要**で、オフライン用の道路地図は同梱していません。地図の点線は訪問順で、実際の道路・鉄道経路ではありません。

予約番号・チケット番号・座席・電話番号・メールアドレス・同行者名・カレンダー本文や非公開リンクは共有版に含めません。自動検査には限界があるため、他人に渡す前に内容を目視で確認します。

## インストール

**Codex専用Skillです。** Codexで利用可能なネイティブ画像生成を優先し、別途のGemini APIキーやローカル画像生成モデルは前提にしません。

### Codexプラグインとして導入

Codex CLIがプラグイン管理をサポートしている場合、OSのターミナルで：

```sh
codex plugin marketplace add usedhonda/seichi-junrei
codex plugin add seichi-junrei@seichi-junrei
```

Codexのチャット・アプリで、実際に表示されるスキルを選ぶか：

```text
$seichi-junrei:seichi-junrei 次の旅行の聖地巡礼候補を3〜5作品、根拠付きで提示して。主役は私が選ぶ。選んだ後はImageGenでオリジナル挿絵を作り、スマホ用ガイドにまとめて。
```

Codex CLIにトップレベルの `/seichi-junrei` コマンドを追加するものではありません。スキルメニュー（`/skills`）など、現在のホストに認識されている呼び出し方を優先してください。

### 直接Skillとして導入する方法

```sh
git clone https://github.com/usedhonda/seichi-junrei.git ~/.agents/skills/seichi-junrei
```

ルートの `SKILL.md` がプラグイン内の共通Skill本体を参照します。この場合は `$seichi-junrei` として見える場合があります。プラグイン版と直接導入版を両方入れる必要はありません。

### 画像生成の利用条件

Codexという名前だけで、画像生成が必ず使えるわけではありません。実行セッションに画像生成ツールがある場合に、表紙・場面絵・スタンプなどを制作します。利用できない場合は、画像制作が未完了であることを伝え、外部APIやローカルモデルを勝手に追加しません。SVGだけの簡易版へ、無断で置き換えることもしません。

画像生成の可否や仕上がりは、利用環境・作品・内容に依存します。希望どおり生成できない場合は、場面・表現・キャラクターの扱いを相談して調整します。「ファンアート」「デフォルメ」という指定が、生成や権利処理を保証するものではありません。

## Skillと制作エンジン

SKILL.mdだけでなく、公開サンプルと同じHTML生成エンジン、テンプレート、動作コード、検証用データを同梱しています。画像は旅行ごとの素材フォルダからHTMLに埋め込みます。

共通エンジンは、複数日の章、日程に連動する地図、場面カード、解説シート、画像拡大、チェックの集計と保存、画像込みのHTML保存を担当します。新しい旅行の調査・行程・文章・画像の生成と選定は、Skillの制作手順に沿って行います。サンプルの制作実績が、あらゆる作品で同じ生成品質を保証するものではありません。

3本のサンプルを360 / 390 / 430 / 520pxで操作検証するCIと、見本を持たない実行環境から別の旅程・素材を生成する検証を同梱しています。実機iPhone／Safariでの検証や、全地点の実地検証は行っていません。[テストの実行結果](https://github.com/usedhonda/seichi-junrei/actions/workflows/test.yml)を確認できます。

## ローカルでデモを動かす（カレンダー接続不要）

Python 3.11以上が必要です。画像をHTML内蔵用に処理するため、**Pillow**を使います。

```bash
git clone https://github.com/usedhonda/seichi-junrei.git
cd seichi-junrei/plugins/seichi-junrei
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# 候補を評価して並べる（主役は自動決定しない）
python3 scripts/rank_candidates.py examples/egypt_candidates.json

# 候補選択用のHTMLを作る
python3 scripts/make_ballot.py examples/egypt_candidates.json --out /tmp/choose.html

# 選択済みのテストデータからスマホガイドを作る
python3 scripts/render_guide.py examples/egypt_guide.json --out /tmp/guide.html

# 出力検査とテスト
python3 scripts/lint_guide.py /tmp/guide.html --guide examples/egypt_guide.json
python3 -m unittest discover -s tests -v
```

`/tmp/choose.html` と `/tmp/guide.html` をブラウザで開いてください。**サンプルJSONの `selection.user_confirmed=true` は動作確認用に設定された架空の選択記録です。実旅行で流用せず、必ずその都度ユーザーの選択を取ります。**

カレンダーのJSONを書き出した場合の補助コマンド：

```bash
python3 scripts/extract_calendar.py examples/calendar_sanitization_test.json --out /tmp/trip.private.json
```

`/tmp/trip.private.json` は*内部作業用*です。共有用HTMLにそのまま入れないでください。

## 利用範囲と権利

**自分や旅仲間と楽しむ、非商用の旅行用しおりを想定しています。画像単体だけでなく、しおり全体の商用利用はお断りしています。** 旅行代理店等の顧客向け資料、ツアー商品への組込み、有料配布・受託制作、広告・集客・販促利用を含み、事業・販促目的の無料配布も対象です。

これは本プロジェクトの制作・利用方針です。**コードとSkill指示はMITライセンスのまま**で、このお願いによってMITの商用利用権を制限するものではありません。GPT Image自体を非商用限定と説明するものでもありません。

公開サンプルの挿絵はGPT Imageで生成した非公式ファンアートで、各作品の権利者から個別の許諾は得ていません。OpenAIとの間での出力の権利帰属と、既存作品・キャラクターの利用許諾は別です。非商用・私的利用の想定や注意書きは、公開サイト・SNSへの掲載に必要な権利確認の代わりにはなりません。

コードとオリジナルのドキュメントは[MITライセンス](LICENSE)、画像・デモ内の図版はその許諾の対象外です。詳細と公式規約へのリンクは[権利と利用方針](plugins/seichi-junrei/references/rights-and-use.md)、素材の扱いは[ASSETS.md](ASSETS.md)を参照してください。作品名・商標は各権利者に帰属し、本プロジェクトは公式・公認サービスではありません。

## リポジトリの中身

`plugins/seichi-junrei/` が単体で動作する共通プラグイン本体です。ルートの `SKILL.md` は直接インストール用の案内です。

| 場所 | 内容 |
| --- | --- |
| [Skill本体](plugins/seichi-junrei/skills/seichi-junrei/SKILL.md) | 旅程の整理、作品選択、調査、制作、品質確認の手順 |
| [references/](plugins/seichi-junrei/references/) | 旅程・調査・アート・権利・データ契約 |
| [scripts/](plugins/seichi-junrei/scripts/) | 旅程抽出、候補評価、選択画面、ガイド生成、検査 |
| [assets/](plugins/seichi-junrei/assets/) | テンプレート、動作コード、ビジュアル素材 |
| [examples/](plugins/seichi-junrei/examples/) | サンプルデータ、調査記録、絵コンテ、生成例 |
| [tests/](plugins/seichi-junrei/tests/) | Python単体テスト、ブラウザ検証、独立環境での生成検証 |

不具合報告・改善提案は[Issues](https://github.com/usedhonda/seichi-junrei/issues)へ。変更の提案は[CONTRIBUTING.md](CONTRIBUTING.md)、脆弱性の連絡は[SECURITY.md](SECURITY.md)を参照してください。
