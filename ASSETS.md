# Asset and content policy / 画像とコンテンツの取り扱い

## しおり全体の非商用方針

本プロジェクトは、自分や旅仲間と楽しむ非商用の旅行用しおりを想定しています。**画像単体に限らず、しおり全体を旅行代理店等の顧客向け資料・ツアー商品・有料配布・受託制作・広告・販促に利用することはお断りしています。** 無料配布でも事業用途を含みます。

これは制作・利用方針であり、コードのMITライセンスを非商用ライセンスに変更するものではありません。MITコードの利用権と図版の権利を混同せず、第三者の権利を本プロジェクトから許諾できるとも扱いません。GPT Imageの出力帰属、公開と私的利用、適用規約の確認結果は[権利と利用方針](plugins/seichi-junrei/references/rights-and-use.md)を参照してください。

## Scope of licenses

The repository's [MIT License](LICENSE) covers original **source code, Skill instructions and original documentation text**. It **does not grant a license to reuse** the separate illustrative media in `plugins/seichi-junrei/assets/stardust/`, `plugins/seichi-junrei/assets/alice/`, the other illustrative media under `plugins/seichi-junrei/assets/`, screenshot images in `docs/`, or embedded illustrations inside `plugins/seichi-junrei/examples/sample-guide.html`.

These examples are shipped so the demonstration can be viewed and tested. **Do not assume the images or franchise-related story content may be separately copied, published, or commercially used** just because the code is open source.

| File(s) | Nature | Notes |
| --- | --- | --- |
| `plugins/seichi-junrei/assets/nile-original.webp`, `plugins/seichi-junrei/assets/nile-portrait.webp` | AI-assisted original illustrative compositions | Not literal photos or geographical proof |
| `plugins/seichi-junrei/assets/temple-original.webp` | AI-assisted stylized temple illustration | Not a site photograph |
| `plugins/seichi-junrei/assets/book-original.webp`, `plugins/seichi-junrei/assets/water-original.webp` | Original abstract scene illustrations | Conceptual imagery, not anime stills |
| `docs/choose-work.png`, `docs/preview-mobile.svg` | Screenshots of the sample workflow | Include the above example art |
| `plugins/seichi-junrei/examples/sample-guide.html` | Self-contained generated demonstration | Contains embedded versions of example illustrations |

## Using your own content

Before publication or distribution:
1. Keep a media-rights manifest with author/creator, original source, usage permission, attribution and restrictions.
2. Use appropriately licensed location photographs and your own imagery; do not download and republish anime screenshots or movie frames without suitable permission.
3. AI-generated art may still raise character, trademark or derivative-work issues. Check rights for the inputs, depicted work and intended use; successful generation or a fan-art label is not permission. Do not republish original frames or claim official endorsement.
4. Label stylized or composite illustrations clearly so they are not mistaken for actual locations or official artwork.
5. Respect applicable official fan-content guidelines where they exist. Private group sharing or noncommercial use is not a blanket exception.

References to titles, creators, scenes and fictional characters in sample data are provided for identification and commentary; they do not imply endorsement or association with their rights holders.

For third-party assets added by contributors, use a separate license/permission entry in the media manifest. If permissions are uncertain, omit the file.


## Mobile engine and new example artwork

`plugins/seichi-junrei/assets/mobile-guide/` contains reusable source CSS and JavaScript covered by the code license. It is the engine used both by installed skills and the public Pages build.

`assets/stardust/` contains the nine original illustrations recovered from the user-approved character-art booklet and later generated companion/transition/closing artwork. `examples/egypt_guide.json` records depicted characters and non-official provenance. Original image bytes are preserved for suitable WebP inputs; their inclusion does not extend the code's MIT license to franchise imagery.

`assets/alice/` contains four Arthur Rackham illustrations from the 1907 edition in [Project Gutenberg eBook 28885](https://www.gutenberg.org/ebooks/28885). The provider identifies the edition as public domain in the USA. The exact source image URLs, creator and descriptions are recorded in `examples/oxford_alice_guide.json`. These are original book illustrations, not AI-generated art, anime frames or Oxford documentary photos. The source edition's reuse notice and applicable territorial status remain relevant.

`docs/stardust-sample.png` and `docs/alice-sample.png` are actual screenshots of outputs from the same renderer. The Oxford example is a model trip for technical/visual validation, not a current reservation or a tested live guided-tour itinerary.
