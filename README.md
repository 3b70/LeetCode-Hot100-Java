# LeetCode Hot 100 Java 完整题解与知识点学习手册

面向Java初学者的中文学习资料。官方题单核对日期：2026-11-25，17专题、100个不同题号。100份源码已通过Java17目标编译及本地测试；没有进行LeetCode官方提交。

<!-- GITHUB_PAGES_DEPLOYMENT -->
## GitHub Pages部署

当前状态：已成功公开发布。GitHub Actions的build与deploy已成功，公网HTTPS首页、专题、题目及资源已实际验证。

- 公开仓库：https://github.com/3b70/LeetCode-Hot100-Java
- 学习网站：https://3b70.github.io/LeetCode-Hot100-Java/
- 唯一发布机制：main → GitHub Actions → Pages；不并行使用gh-deploy。
- 本地检查：`.\.venv\Scripts\python.exe tools/prepare_pages.py`，不重生成题解、Java或PDF。
- 操作及故障排查见[手机与电脑阅读说明](手机与电脑阅读说明.md)，第三方来源见[许可说明](THIRD_PARTY_NOTICES.md)。
- 官方网页快照只在本机留存核对证据，不纳入公开仓库；题目清单及原题链接仍保留。

<!-- END_GITHUB_PAGES_DEPLOYMENT -->

## 手机与电脑阅读

- 本机HTML首页：site/index.html（构建后可双击；公开网址见上方部署状态）：MkDocs Material，100个独立题目页、中文搜索、代码复制、深浅主题。
- [手机与电脑阅读说明](手机与电脑阅读说明.md)：Windows本地阅读、iPhone Safari、主屏幕快捷方式、构建与GitHub Pages手动部署。
- [完整PDF](output/pdf/Hot100-Java-完整学习手册.pdf)：适合保存到iPhone离线阅读。
- 本机网站ZIP包：output/hot100-website.zip（不纳入Git仓库）：解压整个目录后打开index.html。

网站与PDF生成方式、依赖清单和验证范围见阅读说明。网站已通过GitHub Actions公开发布，固定网址见本页顶部。

## 从哪里开始

1. [Java基础知识附录](Java基础知识附录.md)：22项基础与常用API速查。
2. [初学者推荐刷题顺序](初学者推荐刷题顺序.md)：七阶段100题、60天和30天逐日新题/复习安排。
3. [完整学习手册](Hot100-Java-完整学习手册.md)：含全部100题完整讲解与代码，可离线全文搜索。
4. [算法知识附录](算法知识附录.md)：15类算法含义、适用场景、模板和复杂度。
5. 个人学习追踪：本机progress.md（不公开）。
6. [完整性与验证报告](完整性检查报告.md)：检查范围、逐题状态和局限。

本文件位于工作区内新建的LeetCode-Hot100-Java子目录，未改动其他项目。每题九部分统一组织：基本信息、题意、思路、代码、Java知识、示例过程、复杂度、易错点、总结。正文题目仅出现一次，索引与推荐顺序只是导航。

## 专题导航

- [01 哈希（3题）](chapters/01-哈希.md)
- [02 双指针（4题）](chapters/02-双指针.md)
- [03 滑动窗口（2题）](chapters/03-滑动窗口.md)
- [04 子串（3题）](chapters/04-子串.md)
- [05 普通数组（5题）](chapters/05-普通数组.md)
- [06 矩阵（4题）](chapters/06-矩阵.md)
- [07 链表（14题）](chapters/07-链表.md)
- [08 二叉树（15题）](chapters/08-二叉树.md)
- [09 图论（4题）](chapters/09-图论.md)
- [10 回溯（8题）](chapters/10-回溯.md)
- [11 二分查找（6题）](chapters/11-二分查找.md)
- [12 栈（5题）](chapters/12-栈.md)
- [13 堆（3题）](chapters/13-堆.md)
- [14 贪心算法（4题）](chapters/14-贪心算法.md)
- [15 动态规划（10题）](chapters/15-动态规划.md)
- [16 多维动态规划（5题）](chapters/16-多维动态规划.md)
- [17 技巧（5题）](chapters/17-技巧.md)

## 源码、测试与维护

`solutions/`按专题英文目录保存题号开头的源码；普通题类名都是Solution，设计题类名按题意。不能把100份默认包的Solution同时编译到同一个目录。`tests/`是每题的独立测试入口与节点桩，不能混进力扣提交代码。

在本README所在目录执行：

```powershell
python tools/build.py --sources
python tools/verify.py
python tools/build.py
python tools/audit.py
```

需要Python3与JDK17以上。build仅使用Python标准库；verify每题独立编译运行，最多4个并发进程，失败与日志写入`reports/test-results.json`；源码依据`tools/*_content.py`与`tools/content.py`生成，主手册由相同内容的专题章节汇总，避免多处手改。附录源稿在`tools/foundations.py`，文档生成在`tools/render.py`。

## 官方依据

[力扣Hot100官方题单](https://leetcode.cn/studyplan/top-100-liked/)。官方HTML快照：本机sources/official-page.html（不公开）；嵌入数据：本机sources/official-data.json（不公开）；提取后的100题清单：[sources/problems.json](sources/problems.json)。核对时程序断言17组、100题、100唯一题号；未来更新时需重新抓取并审阅，不把旧快照当实时清单。可运行`python tools/extract_official.py`从已保存快照重提取；该操作本身不会联网刷新。

## 文件清单

|题号|名称|难度|讲解|源码|
|---|---|---|---|---|
|1|两数之和|简单|[题解](chapters/01-哈希.md#p1)|[Java](solutions/hash/0001-two-sum.java)|
|49|字母异位词分组|中等|[题解](chapters/01-哈希.md#p49)|[Java](solutions/hash/0049-group-anagrams.java)|
|128|最长连续序列|中等|[题解](chapters/01-哈希.md#p128)|[Java](solutions/hash/0128-longest-consecutive-sequence.java)|
|283|移动零|简单|[题解](chapters/02-双指针.md#p283)|[Java](solutions/two-pointers/0283-move-zeroes.java)|
|11|盛最多水的容器|中等|[题解](chapters/02-双指针.md#p11)|[Java](solutions/two-pointers/0011-container-with-most-water.java)|
|15|三数之和|中等|[题解](chapters/02-双指针.md#p15)|[Java](solutions/two-pointers/0015-3sum.java)|
|42|接雨水|困难|[题解](chapters/02-双指针.md#p42)|[Java](solutions/two-pointers/0042-trapping-rain-water.java)|
|3|无重复字符的最长子串|中等|[题解](chapters/03-滑动窗口.md#p3)|[Java](solutions/sliding-window/0003-longest-substring-without-repeating-characters.java)|
|438|找到字符串中所有字母异位词|中等|[题解](chapters/03-滑动窗口.md#p438)|[Java](solutions/sliding-window/0438-find-all-anagrams-in-a-string.java)|
|560|和为 K 的子数组|中等|[题解](chapters/04-子串.md#p560)|[Java](solutions/substring/0560-subarray-sum-equals-k.java)|
|239|滑动窗口最大值|困难|[题解](chapters/04-子串.md#p239)|[Java](solutions/substring/0239-sliding-window-maximum.java)|
|76|最小覆盖子串|困难|[题解](chapters/04-子串.md#p76)|[Java](solutions/substring/0076-minimum-window-substring.java)|
|53|最大子数组和|中等|[题解](chapters/05-普通数组.md#p53)|[Java](solutions/array/0053-maximum-subarray.java)|
|56|合并区间|中等|[题解](chapters/05-普通数组.md#p56)|[Java](solutions/array/0056-merge-intervals.java)|
|189|轮转数组|中等|[题解](chapters/05-普通数组.md#p189)|[Java](solutions/array/0189-rotate-array.java)|
|238|除了自身以外数组的乘积|中等|[题解](chapters/05-普通数组.md#p238)|[Java](solutions/array/0238-product-of-array-except-self.java)|
|41|缺失的第一个正数|困难|[题解](chapters/05-普通数组.md#p41)|[Java](solutions/array/0041-first-missing-positive.java)|
|73|矩阵置零|中等|[题解](chapters/06-矩阵.md#p73)|[Java](solutions/matrix/0073-set-matrix-zeroes.java)|
|54|螺旋矩阵|中等|[题解](chapters/06-矩阵.md#p54)|[Java](solutions/matrix/0054-spiral-matrix.java)|
|48|旋转图像|中等|[题解](chapters/06-矩阵.md#p48)|[Java](solutions/matrix/0048-rotate-image.java)|
|240|搜索二维矩阵 II|中等|[题解](chapters/06-矩阵.md#p240)|[Java](solutions/matrix/0240-search-a-2d-matrix-ii.java)|
|160|相交链表|简单|[题解](chapters/07-链表.md#p160)|[Java](solutions/linked-list/0160-intersection-of-two-linked-lists.java)|
|206|反转链表|简单|[题解](chapters/07-链表.md#p206)|[Java](solutions/linked-list/0206-reverse-linked-list.java)|
|234|回文链表|简单|[题解](chapters/07-链表.md#p234)|[Java](solutions/linked-list/0234-palindrome-linked-list.java)|
|141|环形链表|简单|[题解](chapters/07-链表.md#p141)|[Java](solutions/linked-list/0141-linked-list-cycle.java)|
|142|环形链表 II|中等|[题解](chapters/07-链表.md#p142)|[Java](solutions/linked-list/0142-linked-list-cycle-ii.java)|
|21|合并两个有序链表|简单|[题解](chapters/07-链表.md#p21)|[Java](solutions/linked-list/0021-merge-two-sorted-lists.java)|
|2|两数相加|中等|[题解](chapters/07-链表.md#p2)|[Java](solutions/linked-list/0002-add-two-numbers.java)|
|19|删除链表的倒数第 N 个结点|中等|[题解](chapters/07-链表.md#p19)|[Java](solutions/linked-list/0019-remove-nth-node-from-end-of-list.java)|
|24|两两交换链表中的节点|中等|[题解](chapters/07-链表.md#p24)|[Java](solutions/linked-list/0024-swap-nodes-in-pairs.java)|
|25|K 个一组翻转链表|困难|[题解](chapters/07-链表.md#p25)|[Java](solutions/linked-list/0025-reverse-nodes-in-k-group.java)|
|138|随机链表的复制|中等|[题解](chapters/07-链表.md#p138)|[Java](solutions/linked-list/0138-copy-list-with-random-pointer.java)|
|148|排序链表|中等|[题解](chapters/07-链表.md#p148)|[Java](solutions/linked-list/0148-sort-list.java)|
|23|合并 K 个升序链表|困难|[题解](chapters/07-链表.md#p23)|[Java](solutions/linked-list/0023-merge-k-sorted-lists.java)|
|146|LRU 缓存|中等|[题解](chapters/07-链表.md#p146)|[Java](solutions/linked-list/0146-lru-cache.java)|
|94|二叉树的中序遍历|简单|[题解](chapters/08-二叉树.md#p94)|[Java](solutions/binary-tree/0094-binary-tree-inorder-traversal.java)|
|104|二叉树的最大深度|简单|[题解](chapters/08-二叉树.md#p104)|[Java](solutions/binary-tree/0104-maximum-depth-of-binary-tree.java)|
|226|翻转二叉树|简单|[题解](chapters/08-二叉树.md#p226)|[Java](solutions/binary-tree/0226-invert-binary-tree.java)|
|101|对称二叉树|简单|[题解](chapters/08-二叉树.md#p101)|[Java](solutions/binary-tree/0101-symmetric-tree.java)|
|543|二叉树的直径|简单|[题解](chapters/08-二叉树.md#p543)|[Java](solutions/binary-tree/0543-diameter-of-binary-tree.java)|
|102|二叉树的层序遍历|中等|[题解](chapters/08-二叉树.md#p102)|[Java](solutions/binary-tree/0102-binary-tree-level-order-traversal.java)|
|108|将有序数组转换为二叉搜索树|简单|[题解](chapters/08-二叉树.md#p108)|[Java](solutions/binary-tree/0108-convert-sorted-array-to-binary-search-tree.java)|
|98|验证二叉搜索树|中等|[题解](chapters/08-二叉树.md#p98)|[Java](solutions/binary-tree/0098-validate-binary-search-tree.java)|
|230|二叉搜索树中第 K 小的元素|中等|[题解](chapters/08-二叉树.md#p230)|[Java](solutions/binary-tree/0230-kth-smallest-element-in-a-bst.java)|
|199|二叉树的右视图|中等|[题解](chapters/08-二叉树.md#p199)|[Java](solutions/binary-tree/0199-binary-tree-right-side-view.java)|
|114|二叉树展开为链表|中等|[题解](chapters/08-二叉树.md#p114)|[Java](solutions/binary-tree/0114-flatten-binary-tree-to-linked-list.java)|
|105|从前序与中序遍历序列构造二叉树|中等|[题解](chapters/08-二叉树.md#p105)|[Java](solutions/binary-tree/0105-construct-binary-tree-from-preorder-and-inorder-traversal.java)|
|437|路径总和 III|中等|[题解](chapters/08-二叉树.md#p437)|[Java](solutions/binary-tree/0437-path-sum-iii.java)|
|236|二叉树的最近公共祖先|中等|[题解](chapters/08-二叉树.md#p236)|[Java](solutions/binary-tree/0236-lowest-common-ancestor-of-a-binary-tree.java)|
|124|二叉树中的最大路径和|困难|[题解](chapters/08-二叉树.md#p124)|[Java](solutions/binary-tree/0124-binary-tree-maximum-path-sum.java)|
|200|岛屿数量|中等|[题解](chapters/09-图论.md#p200)|[Java](solutions/graph/0200-number-of-islands.java)|
|994|腐烂的橘子|中等|[题解](chapters/09-图论.md#p994)|[Java](solutions/graph/0994-rotting-oranges.java)|
|207|课程表|中等|[题解](chapters/09-图论.md#p207)|[Java](solutions/graph/0207-course-schedule.java)|
|208|实现 Trie (前缀树)|中等|[题解](chapters/09-图论.md#p208)|[Java](solutions/graph/0208-implement-trie-prefix-tree.java)|
|46|全排列|中等|[题解](chapters/10-回溯.md#p46)|[Java](solutions/backtracking/0046-permutations.java)|
|78|子集|中等|[题解](chapters/10-回溯.md#p78)|[Java](solutions/backtracking/0078-subsets.java)|
|17|电话号码的字母组合|中等|[题解](chapters/10-回溯.md#p17)|[Java](solutions/backtracking/0017-letter-combinations-of-a-phone-number.java)|
|39|组合总和|中等|[题解](chapters/10-回溯.md#p39)|[Java](solutions/backtracking/0039-combination-sum.java)|
|22|括号生成|中等|[题解](chapters/10-回溯.md#p22)|[Java](solutions/backtracking/0022-generate-parentheses.java)|
|79|单词搜索|中等|[题解](chapters/10-回溯.md#p79)|[Java](solutions/backtracking/0079-word-search.java)|
|131|分割回文串|中等|[题解](chapters/10-回溯.md#p131)|[Java](solutions/backtracking/0131-palindrome-partitioning.java)|
|51|N 皇后|困难|[题解](chapters/10-回溯.md#p51)|[Java](solutions/backtracking/0051-n-queens.java)|
|35|搜索插入位置|简单|[题解](chapters/11-二分查找.md#p35)|[Java](solutions/binary-search/0035-search-insert-position.java)|
|74|搜索二维矩阵|中等|[题解](chapters/11-二分查找.md#p74)|[Java](solutions/binary-search/0074-search-a-2d-matrix.java)|
|34|在排序数组中查找元素的第一个和最后一个位置|中等|[题解](chapters/11-二分查找.md#p34)|[Java](solutions/binary-search/0034-find-first-and-last-position-of-element-in-sorted-array.java)|
|33|搜索旋转排序数组|中等|[题解](chapters/11-二分查找.md#p33)|[Java](solutions/binary-search/0033-search-in-rotated-sorted-array.java)|
|153|寻找旋转排序数组中的最小值|中等|[题解](chapters/11-二分查找.md#p153)|[Java](solutions/binary-search/0153-find-minimum-in-rotated-sorted-array.java)|
|4|寻找两个正序数组的中位数|困难|[题解](chapters/11-二分查找.md#p4)|[Java](solutions/binary-search/0004-median-of-two-sorted-arrays.java)|
|20|有效的括号|简单|[题解](chapters/12-栈.md#p20)|[Java](solutions/stack/0020-valid-parentheses.java)|
|155|最小栈|中等|[题解](chapters/12-栈.md#p155)|[Java](solutions/stack/0155-min-stack.java)|
|394|字符串解码|中等|[题解](chapters/12-栈.md#p394)|[Java](solutions/stack/0394-decode-string.java)|
|739|每日温度|中等|[题解](chapters/12-栈.md#p739)|[Java](solutions/stack/0739-daily-temperatures.java)|
|84|柱状图中最大的矩形|困难|[题解](chapters/12-栈.md#p84)|[Java](solutions/stack/0084-largest-rectangle-in-histogram.java)|
|215|数组中的第K个最大元素|中等|[题解](chapters/13-堆.md#p215)|[Java](solutions/heap/0215-kth-largest-element-in-an-array.java)|
|347|前 K 个高频元素|中等|[题解](chapters/13-堆.md#p347)|[Java](solutions/heap/0347-top-k-frequent-elements.java)|
|295|数据流的中位数|困难|[题解](chapters/13-堆.md#p295)|[Java](solutions/heap/0295-find-median-from-data-stream.java)|
|121|买卖股票的最佳时机|简单|[题解](chapters/14-贪心算法.md#p121)|[Java](solutions/greedy/0121-best-time-to-buy-and-sell-stock.java)|
|55|跳跃游戏|中等|[题解](chapters/14-贪心算法.md#p55)|[Java](solutions/greedy/0055-jump-game.java)|
|45|跳跃游戏 II|中等|[题解](chapters/14-贪心算法.md#p45)|[Java](solutions/greedy/0045-jump-game-ii.java)|
|763|划分字母区间|中等|[题解](chapters/14-贪心算法.md#p763)|[Java](solutions/greedy/0763-partition-labels.java)|
|70|爬楼梯|简单|[题解](chapters/15-动态规划.md#p70)|[Java](solutions/dp/0070-climbing-stairs.java)|
|118|杨辉三角|简单|[题解](chapters/15-动态规划.md#p118)|[Java](solutions/dp/0118-pascals-triangle.java)|
|198|打家劫舍|中等|[题解](chapters/15-动态规划.md#p198)|[Java](solutions/dp/0198-house-robber.java)|
|279|完全平方数|中等|[题解](chapters/15-动态规划.md#p279)|[Java](solutions/dp/0279-perfect-squares.java)|
|322|零钱兑换|中等|[题解](chapters/15-动态规划.md#p322)|[Java](solutions/dp/0322-coin-change.java)|
|139|单词拆分|中等|[题解](chapters/15-动态规划.md#p139)|[Java](solutions/dp/0139-word-break.java)|
|300|最长递增子序列|中等|[题解](chapters/15-动态规划.md#p300)|[Java](solutions/dp/0300-longest-increasing-subsequence.java)|
|152|乘积最大子数组|中等|[题解](chapters/15-动态规划.md#p152)|[Java](solutions/dp/0152-maximum-product-subarray.java)|
|416|分割等和子集|中等|[题解](chapters/15-动态规划.md#p416)|[Java](solutions/dp/0416-partition-equal-subset-sum.java)|
|32|最长有效括号|困难|[题解](chapters/15-动态规划.md#p32)|[Java](solutions/dp/0032-longest-valid-parentheses.java)|
|62|不同路径|中等|[题解](chapters/16-多维动态规划.md#p62)|[Java](solutions/multidimensional-dp/0062-unique-paths.java)|
|64|最小路径和|中等|[题解](chapters/16-多维动态规划.md#p64)|[Java](solutions/multidimensional-dp/0064-minimum-path-sum.java)|
|5|最长回文子串|中等|[题解](chapters/16-多维动态规划.md#p5)|[Java](solutions/multidimensional-dp/0005-longest-palindromic-substring.java)|
|1143|最长公共子序列|中等|[题解](chapters/16-多维动态规划.md#p1143)|[Java](solutions/multidimensional-dp/1143-longest-common-subsequence.java)|
|72|编辑距离|中等|[题解](chapters/16-多维动态规划.md#p72)|[Java](solutions/multidimensional-dp/0072-edit-distance.java)|
|136|只出现一次的数字|简单|[题解](chapters/17-技巧.md#p136)|[Java](solutions/tricks/0136-single-number.java)|
|169|多数元素|简单|[题解](chapters/17-技巧.md#p169)|[Java](solutions/tricks/0169-majority-element.java)|
|75|颜色分类|中等|[题解](chapters/17-技巧.md#p75)|[Java](solutions/tricks/0075-sort-colors.java)|
|31|下一个排列|中等|[题解](chapters/17-技巧.md#p31)|[Java](solutions/tricks/0031-next-permutation.java)|
|287|寻找重复数|中等|[题解](chapters/17-技巧.md#p287)|[Java](solutions/tricks/0287-find-the-duplicate-number.java)|
