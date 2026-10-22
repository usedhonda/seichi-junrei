# 勝手に聖地巡礼 — seichi-junrei

**旅行予定を見せるだけ。旅先にゆかりのあるアニメ・漫画・映画をAIが探し、あなたが選んだ物語で、旅仲間向けのスマホガイドを作るSkill。**

[![Tests](https://github.com/usedhonda/seichi-junrei/actions/workflows/test.yml/badge.svg)](https://github.com/usedhonda/seichi-junrei/actions/workflows/test.yml)
[![MIT License](https://img.shields.io/badge/code%20license-MIT-blue.svg)](LICENSE)
[![Skill](https://img.shields.io/badge/Agent-Skill-8b5cf6.svg)](SKILL.md)

![スマホガイドのサンプル](docs/preview-mobile.svg)

> **「今度の旅、勝手に聖地巡礼にして。」**
>
> *Turn an ordinary itinerary into a story-driven pilgrimage for your travel companions.*

## インストール：Claude Code（CC）／Codex（CDX）

**makeloopと同じく、Claude Code用とCodex用のマーケットプレイスを備えたプラグイン**です。共通の本体は `plugins/seichi-junrei/skills/seichi-junrei/SKILL.md`。両ホストで**3〜5作品の候補を提示→ユーザーが主役を選択→旅のしおり制作**の流れは同じです。

### Claude Code（CC）

Claude Codeの入力欄で順番に実行：

```text
/plugin marketplace add usedhonda/seichi-junrei
/plugin install seichi-junrei@seichi-junrei
```

インストール後、スラッシュメニューに表示される `/seichi-junrei:seichi-junrei` を選んでください。

```text
/seichi-junrei:seichi-junrei 次の旅行に合う聖地巡礼候補を3〜5作品提案して。作品は私が選ぶ。
```

### Codex（CDX）

Codex CLIが利用できる**OSのターミナル**で：

```sh
codex plugin marketplace add usedhonda/seichi-junrei
codex plugin add seichi-junrei@seichi-junrei
```

Codexのチャット入力欄またはスキルメニュー（`/skills`）で：

```text
$seichi-junrei:seichi-junrei 次の旅行で聖地巡礼できる作品を3〜5本、根拠付きで提案して。選ぶのは私。
```

**Codexにトップレベルの `/seichi-junrei` コマンドを追加しているわけではありません。** 必ずホストが実際に認識しているSkillを利用してください。

### 直接導入（CodexのAgent Skillとして使う場合）

```sh
git clone https://github.com/usedhonda/seichi-junrei.git ~/.agents/skills/seichi-junrei
```

この場合は `$seichi-junrei` として見えることがあります。ルート `SKILL.md` は**共通本体を読むだけの互換ラッパー**です。重複登録を避けるため、通常はプラグイン方式・直接導入方式のどちらか一方を選びます。

> **アクセス権限について**：このSkillを入れるだけでGoogleカレンダー・ブラウザ・画像生成・Sitesにアクセスできるわけではありません。実際に接続済みのツールを使用し、利用できないときは旅程テキストなどを受け取ります。Pythonで画像をHTMLに内蔵するときはプラグイン内の `requirements.txt` の依存関係が必要です。公開はオプションで、勝手に公開しません。


## 何ができる？

旅行のフライト・ホテル・滞在先から、**その土地と本当に関係のある作品を3〜5本提案**。好きな作品を選んだら、作品の名場面と現地の見どころをつないだ、読み物として楽しい旅のしおりを制作します。

| ステップ | AIが行うこと | あなたが行うこと |
| --- | --- | --- |
| ① 旅行を把握 | 接続済みGoogleカレンダーなどから移動・宿泊・自由時間を読み取る | 旅行を指定する |
| ② 作品を発見 | アニメ・漫画・映画など3〜5作品を関連の根拠付きで提示 | **主役1作品を選ぶ**（寄り道作品は最大2本） |
| ③ 聖地を検証 | アニメ話数・漫画巻数・映画のシーン、実際の舞台・ロケ地を照合 | 必要なときだけ方向性を伝える |
| ④ 旅を編集 | 実際の訪問順に、物語・歴史・観光情報を編み直す | 読んで楽しむ |
| ⑤ ビジュアル制作 | 現地の画像と権利に配慮した独自イラストを組み合わせる | デザイン見本を指定してもよい |
| ⑥ 完成 | 画像を埋め込んだ**オフラインでも読める単一HTML**を検証して渡す | 旅仲間と共有する |

**作品の選択は必須の停止点です。** AIが候補の1位を勝手に採用したり、選ばれる前に本編を作ったりしません。「おまかせ」と明示された場合だけ選定を委任できます。

### 完成イメージ

| 候補を選ぶ | 旅先で読む |
| --- | --- |
| ![作品候補を選ぶ画面](docs/choose-work.png) | ![旅ガイドの画面](docs/preview-mobile.svg) |

**[サンプルのHTML](plugins/seichi-junrei/examples/sample-guide.html)** はジョジョ第3部とアスワン・アブ・シンベルを題材にした*説明用デモ*です。公式作品ではありません。デモの日付・内容は実際の旅行の予約情報ではありません。

### 会話の例

**ユーザー：**「今週末の旅行を聖地巡礼ツアーにして」

**AI：**「旅程はアスワン → アブ・シンベル。候補は『ジョジョの奇妙な冒険 第3部』『ナイル殺人事件（1978）』『ハムナプトラ（1999）』です。作品の舞台なのか、ロケ地なのか、単にテーマが近いだけなのかも分けて説明します。どれを主役にしますか？」

**ユーザー：**「ジョジョを主役に。あとは任せる」

**AI：** 第25〜29話と現地の場所を確認し、聖地と単なる連想スポットを区別。アニメの場面の振り返り・歴史・見どころを交え、スマホで読めるHTMLを制作。

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

## 聖地の事実を守る

「作品の舞台」「実際のロケ地」「公式に確認できるモデル」「雰囲気が似ているだけ」は別物です。これらを混同せず、話数・巻数・シーン・地図・開館情報も根拠付きで確認します。裏付けがなければ聖地とは断定しません。

**画像についても、「AI生成＝自由に使えるファンアート」とは限りません。** キャラクターの特徴や既存カットの再現を避け、適切な権利確認ができる素材を使います。詳しくは[アセットの扱い](ASSETS.md)と[編集・アート方針](references/editorial-and-art.md)を参照してください。

## プライバシーと共有

標準成果物は **単一HTMLファイル**。公開URLやアカウントは不要です。旅仲間とのAirDrop・ファイル共有を想定し、画像は原則内蔵します。公開サイトを作るのはユーザーが明示的に希望した場合だけです。

予約番号・チケット番号・座席・電話番号・メールアドレス・同行者名・カレンダーの本文や非公開リンクは共有版に含めません。抽出スクリプトも元の予定タイトルをそのまま出力しません。ただし自動検査は万能ではないため、**他人に渡す前の目視確認は必須**です。

## リポジトリの中身

`plugins/seichi-junrei/` がインストール単体で動作する**共通プラグイン本体**です。ルートの `SKILL.md` は直接インストール用ラッパーに過ぎません。


| ディレクトリ | 役割 |
| --- | --- |
| [Skill本体](plugins/seichi-junrei/skills/seichi-junrei/SKILL.md) | エージェントの手順と選択・調査・品質ゲート |
| [Skill表示設定](plugins/seichi-junrei/skills/seichi-junrei/agents/openai.yaml) | Skillメタデータ |
| [references/](plugins/seichi-junrei/references/) | 旅程・根拠・制作・データ契約 |
| [scripts/](plugins/seichi-junrei/scripts/) | 旅程抽出／候補順位／選択UI／ガイド生成／検査 |
| [assets/](plugins/seichi-junrei/assets/) | 説明用の独自ビジュアル素材 |
| [examples/](plugins/seichi-junrei/examples/) | 説明用データと生成例 |
| [tests/](plugins/seichi-junrei/tests/) | 画面検証補助とPython単体テスト |

ホストによる呼び出し・制限の違いは[CC/CDX互換ガイド](plugins/seichi-junrei/references/hosts.md)を参照。Claude CodeとCodexのSkillは**1本の本体**を共有し、今後も二重管理しません。

## 協力・ライセンス

不具合報告や改善提案はIssueへ。コードの変更は[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。脆弱性の連絡方法は[SECURITY.md](SECURITY.md)に記載しています。

**コードとオリジナルのドキュメントはMITライセンス**です（[LICENSE](LICENSE)）。画像・デモ内の図版はこのMIT許諾の対象外です。取り扱いは[ASSETS.md](ASSETS.md)を確認してください。作品名や商標は各権利者に帰属します。本プロジェクトは各作品の公式・公認サービスではありません。

---

<small>seichi-junrei · 勝手に聖地巡礼 · 旅先を「知っている物語」の中にする。</small>
