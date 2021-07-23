# News Classification for CTBC-INVESTMENT

# 標籤規格
- Negative 新聞
    - 因為是風控要求，故只需要鎖定負面新聞即可
    - 不用判斷正面與中性
- ESG 新聞
    - 同 Negative 新聞
    - ESG新聞先請投信同仁提供範例
    - 數研發分析後，再設計算法計算ESG之正負面程度

```
@dataclass
class SpecStruct:

    NN: bool
    NN_SCORE: float
    NN_KEYWORDS: List[str]
    ESG: bool
    ESG_SCORE: float
    ESG_KEYWORDS: List[str]
    DEBUG: Dict[str, List[Dict[str, str]]] = field(default_factory=dict)

    def __repr__(self):
        return (
            f"[      NN      ]: {self.NN}\n"
            f"[   NN_SCORE   ]: {self.NN_SCORE}\n"
            f"[  NN_KEYWORDS ]: {self.NN_KEYWORDS}\n"
            f"[      ESG     ]: {self.ESG}\n"
            f"[   ESG_SCORE  ]: {self.ESG_SCORE}\n"
            f"[ ESG_KEYWORDS ]: {self.ESG_KEYWORDS}\n"
            f"[     DEBUG    ]: See details below.\n"
        ) + (
            "\n".join(
                f"{cate}:{i}: {d['keywords']} ==> {d['text']}"
                for cate, details in self.DEBUG.items()
                for i, d in enumerate(details)
            )
            if self.DEBUG
            else ("DEBUG is False. So Nothing is in DEBUG.")
        )
```


# API
## 準備 Production 環境 (Optional if aleardy prepared)
```
$ conda create --name NewsClassifier-py38 python=3.8 
$ conda activate NewsClassifier-py38
$ make prepare_production_env
```

## 分類新聞
```
from src.utils import struct as st
from src.SimpleComparator import SimpleComparator

""" Init reader """
nn_reader = SimpleComparator(category="Negative_News")
esg_reader = SimpleComparator(category="ESG_News")

""" Classify News """
nn_res = nn_reader.classify(news_title="xxxx", news_body="mmmm")
esg_res = esg_reader.classify(news_title="yyyy", news_body="nnnn")

""" Spec Format """
sc_ret = st.SpecStruct(
    NN = True if nn_res.news_category == st.NewsCategory.NN else False,
    NN_SCORE = nn_res.score,
    NN_KEYWORDS = nn_res.keywords,
    ESG = True if esg_res.news_category == st.NewsCategory.ESG else False,
    ESG_SCORE = esg_res.score,
    ESG_KEYWORDS = esg_res.keywords,
)
```

### Noted
1. Debug 模式

    - 如何調用

        當使用者想查看新聞的哪些句子出現了哪些關鍵詞而導致判斷該新聞為 Negative / ESG 時，可以開啟 Debug 模式來查看情況。
        ```
        """ Init reader """
        nn_reader = SimpleComparator(category="Negative_News", debug=True) <-- 開啟 Debug mode
        esg_reader = SimpleComparator(category="ESG_News", debug=True) <-- 開啟 Debug mode

        """ Classify News """
        nn_res = nn_reader.classify(news_title = "xxxx", news_body = "mmmmm")
        esg_res = esg_reader.classify(news_title = "yyyy", news_body = "nnnn")

        """ Spec Format """
        sc_ret = st.SpecStruct(
            NN = True if nn_res.news_category == st.NewsCategory.NN else False,
            NN_SCORE = nn_res.score,
            NN_KEYWORDS = nn_res.keywords,
            ESG = True if esg_res.news_category == st.NewsCategory.ESG else False,
            ESG_SCORE = esg_res.score,
            ESG_KEYWORDS = esg_res.keywords,
            DEBUG={"NN": nn_res.debug, "ESG": esg_res.debug}, <-- 收集 Debug 資訊
        )
        ```

2. 計分方式

    - 新聞標題的權重 > 新聞內文的權重

        舉例來說: title_weight = 0.3, body_weight = 0.1，$\frac{title}{body} = \frac{0.3}{0.1} = <u>3</u>$。
        當新聞標題 (news_title) 出現 p 個關鍵字，新聞內文 (news_body) 出現 q 個關鍵字時，實際上，程式會以 $k=3*p+q$ 個關鍵詞去計分。
        
        $$
            score(k)=\begin{cases}
                0, k = 0\\
                0.50 + \frac{0.50}{(15^2)} \cdot k^2, 0< k < 16\\
                1.00, otherwise
            \end{cases}
        $$ 
        
        詳請可見 `src::SimpleComparator::score_func`

    - 如何調用

        若要改變 title_weight 和 body_weight，可於 classify function 中傳入 argument。這代表可以針對不同的新聞去做客製化的調配。
        ```
        """ Classify News """
        ## 設定 nn_reader 在判讀這篇新聞時，title_weight=0.7, body_weight=0.3
        nn_res = nn_reader.classify(news_title = "xxxx", news_body = "mmmmm", title_weight=0.7, body_weight=0.2)

        ## 設定 esg_reader 在判讀這篇新聞，使用預設值 (title_weight=0.3, body_weight=0.1)
        esg_res = esg_reader.classify(news_title = "yyyy", news_body = "nnnn")
        ```
    
3. 判斷方式

    - 閾值判斷

        針對不同的 SimpleComparator，透過計分方式，每篇新聞可以得出一個分數。當此分數大於**threshold** (default=0.50)時，則判定該新聞為某一類新聞，反之則否。
        
    - 如何調用

        若要改變閾值，可在 classify function 中傳入 argument。這代表可以針對不同的新聞去做客製化的調配。
        ```
        """ Classify News """
        ## 設定 nn_reader 在判讀這篇新聞時，threshold=0.7
        nn_res = nn_reader.classify(news_title = "xxxx", news_body = "mmmmm", threshold=0.7)

        ## 設定 esg_reader 在判讀這篇新聞，使用預設值 (threshold=0.5)
        esg_res = esg_reader.classify(news_title = "yyyy", news_body = "nnnn")
        ```
    
## 產出關鍵字
```
from datetime import datetime
from src.KeyGenerator.KeyGenerator import Word2VecKeyGenerator

w2v = Word2VecKeyGenerator(modelkey="20210603040434")

""" NN """
now = datetime.now().strftime("%Y%m%d%H%M%S")
nn_file = "src/utils/keywords/negative_news/NN_keywords.txt"
nn_outfile_json = f"src/utils/keywords/negative_news/NN_keywords_{now}.json"
nn_outfile_txt = f"src/utils/keywords/negative_news/NN_keywords_{now}.txt"

w2v.infer(nn_file)
w2v.save2json(outfile=nn_outfile_json)
w2v.save2txt(outfile=nn_outfile_txt)

""" ESG """
now = datetime.now().strftime("%Y%m%d%H%M%S")
esg_file = "src/utils/keywords/esg_news/ESG_keywords.txt"
esg_outfile_json = f"src/utils/keywords/esg_news/ESG_keywords_{now}.json"
esg_outfile_txt = f"src/utils/keywords/esg_news/ESG_keywords_{now}.txt"

w2v.infer(esg_file)
w2v.save2json(outfile=esg_outfile_json)
w2v.save2txt(outfile=esg_outfile_txt)
```

### Noted

1. 原理

    - Word2Vec
    
        使用 Word2Vec 模型與大量維基文本進行訓練，使每個詞都擁有一個多維向量，從這多維空間中，找出座標相近的點作為相關詞。
        何謂座標相近呢？我採用餘弦值作為衡量指標，當空間中兩點距離越近，餘弦夾角越小，餘弦值越大，注意此處有做正規化，撇除兩點空間距離很遠，夾角很小的例子。
        但是餘弦衡量標準無法輸出同義詞和反義詞的差別，因為 Word2Vec 在訓練向量時，是以單詞的前後文來做向量運算，而同義詞和反義詞的前後文雷同，導致其向量相近，故餘弦值亦大。
        因此，此 API 僅能產出相關詞，而非同義詞或反義詞，仍須以人為判斷為主。

    - 訓練細節
    
        詳見 https://github.com/allenyummy/Word2Vec

2. 推論

    - topn (default=10)
        
        針對每個關鍵詞，輸出 topn 個相關詞。此設定為全域值，每個關鍵字都以此為依歸。
        ```
        w2v.infer("xxx.txt", topn=25)
        ```
        
    - threshold (default=0.70, 最大為1.0)

        針對每個關鍵詞，輸出 topn 個相關詞。此設定為全域值，每個關鍵字都以此為依歸。
        ```
        w2v.infer("xxx.txt", threshold=0.82)
        ```

    - force_info (default=None, type=dict)

        若有些關鍵字有特殊要求，想要設定不同的 topn/threshold，可於此處設定。
        ```
        force_info = {
            "暴力": {
                "topn": 10,
                "threshold": 0.44,
            },
            "下跌": {
                "topn": 4,
                "threshold": 0.83,
            }
            ...
        }
        w2v.infer("xxx.txt", force_info=force_info)
        ```

    - init_results (default=True)

        每次執行 infer function 時，都會將結果存放在 self.results 裡。
        因此，若需從頭開始，則可以傳入此 argument。建議勿將其改成 False，以免使得結果混亂而不知從何 debug。
        ```
        w2v.infer(nn_file, topn, threshold, force_info=None, init_results=True)
        ```

3. 寫檔

    - 輸出 json 格式 (For internal use)

        輸出成 json 格式，裡頭會記載所有細節，包含 createtime, modelkey, use_fast, base, default_info, force_info, results。
        此檔為 debug 使用，觀察模型輸出狀況。建議以時間來命名。
        ```
        w2v.save2json(outfile="xxx.json")
        ```
    
    - 輸出 txt 格式 (For deliver)
        
        輸出成 txt 格式，每一列表示一個關鍵字。
        ```
        w2v.save2txt(outfile="yyy.json")
        ```

# 開發模式

## 準備 Development 環境 (Optional if aleardy prepared)
```
$ conda create --name NewsClassifier-py38 python=3.8 
$ conda activate NewsClassifier-py38
$ make prepare_dev_env
```

### Noted
0. 若將 conda command 寫進 makfile 中，有一些路徑問題需要解決，故索性先不處理，若有必要，再處理。

1. 安裝額外的套件於此開發環境 (extras packages would be installed)
    ```
    $ poetry install -E [xxx]
    $ poetry install -E excel  ## 範例: 將會安裝 excel 相關的套件 [pandas, xlrd, openpyxl]
    ```
    Note: [xxx] 詳見 `pyproject.toml`

2. 展示套件狀況
    
    - 開發環境**所有套件** (全部寫在 `pyproject.toml` 裡)

        藍色代表已安裝在 `NewsClassifier-py38` 環境中；紅色代表未安裝於環境中的套件 (都是 extras 套件)。
        ```
        $ make show
        ```

    - 展示開發環境**所有套件**相依狀況
        在 terminal 上可以看到七彩的套件與其相依性。另外，本地端也存有一個黑白檔案，名為 dependencies.txt，供紀錄使用。
        注意該指令也會把 extras 套件也都列出來，
        ```
        $ make show_dependency
        `
3. 開發過程須知
    
    - 格式/語法/檢查
    
        本地端開發時，使用`git commit -m "..."`時，會自動進行 pre-commit 測試，確保格式/語法無誤方能 commit 至本地端，減少 push 至 repo 時，CI/CD pipeline 因語法錯誤而中斷。測試項目詳見 `.pre-commit-config.yaml`
        
    - 演算法邏輯測試: 待完成中。


## 開發中
- Show dependencies among words by networkx
