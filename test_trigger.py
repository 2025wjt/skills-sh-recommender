import sys

sys.path.insert(
    0, r"C:\Users\jackw\.config\opencode\skills\superpowers\skills-sh-recommender"
)

from skill_detector import is_skill_query

test_cases = [
    "有什么视频相关的 skill？",
    "推荐一个前端 skill",
    "帮我搜索 react skill",
    "我想用 React 创建网站",
    "项目需要 ffmpeg 处理视频",
]

for test in test_cases:
    result = is_skill_query(test)
    print(f"Input: {test}")
    print(f"Result: {result}")
    print()
