from __future__ import annotations

from wechat_mcp.mcp_server import global_search


def main() -> None:
    print(global_search("John"))


if __name__ == "__main__":
    main()
