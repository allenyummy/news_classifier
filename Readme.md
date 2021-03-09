# News Classification for CTBC-INV

## 標籤規格:
- 新聞正負面：
    - 因為是風控要求，故只需要鎖定負面新聞即可.
    - 不用判斷正面與中性
- ESG新聞：
    - ESG新聞先請投信同仁提供範例
    - 數研發分析後，再設計算法計算ESG之正負面程度

## API開發:
- 開發環境:
    - Windows + python 3.6

## Quick Start:
(1) Init: 
pip install -r requirements.txt

(2) Run example.
python example.py
```bash
$ python example.py
news_samples/dowjones/CHTOTW0020160129ec1u0007d.json 被控掏空公司、詐補助款、買盜伐木 悠活前董座涉詐 獲利上億元
{'NN': True, 'NN_SCORE': 100, 'NN_KEYWORDS': ['掏空', '起訴', '不法', '非法', '背信', '挪用', '涉案', '虛報', '詐取', '傷害', '違反', '檢察'], 'ESG': False, 'ESG_SCORE': 0}
news_samples/dowjones/LIBTOT0020170303ed3400056.json 出獄繼續騙 身背7條通緝
{'NN': True, 'NN_SCORE': 100, 'NN_KEYWORDS': ['犯罪', '告發', '侵害', '涉嫌', '起訴', '判刑', '判決', '判處', '指控', '控告', '殺害', '被告', '撤銷', '誘騙', '檢察'], 'ESG': False, 'ESG_SCORE': 0}
news_samples/dowjones/LIBTOT0020190220ef2l0001j.json 愛國同心會長涉賄選 檢不排除有中資
{'NN': True, 'NN_SCORE': 100, 'NN_KEYWORDS': ['起訴', '非法', '違反', '不法', '犯罪', '賄賂', '檢舉'], 'ESG': False, 'ESG_SCORE': 0}
news_samples/dowjones/CTRTOT0020170125ed1p000uw.json 暴力討債炒股審理逾8年 鄒興華16人減刑
{'NN': True, 'NN_SCORE': 100, 'NN_KEYWORDS': ['炒股', '判刑', '判決', '上訴', '地下錢莊', '侵害', '起訴', '有罪', '涉案', '被告', '違反', '罰金'], 'ESG': False, 'ESG_SCORE': 0}
...
```


(Optional) Run tests.
```bash
$make test
nosetests -v tests
test_absolute_truth_and_meaning (test_basic.BasicTestSuite) ... ok
test_class_init (test_biznews.BasicTestSuite) ... ok
Test the return format of the class. ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.004s

OK
```
