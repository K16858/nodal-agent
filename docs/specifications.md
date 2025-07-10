# Nodal-Agent

## 概要
- 目的：JSONで定義されたグラフ構造の世界で、LLM搭載のエージェントが自律的に行動する
シミュレーションを構築する。
- コアコンセプト
    - データ駆動：世界の構造（場所、オブジェクト、接続関係）は外部のJSONファイルによって定義される
    - グラフ構造：場所間の移動は、定義された接続関係にのみ限定される
    - 動的行動：エージェントが実行可能な行動は、その場の状況（場所、所持品』，他者の存在）によって動的に制限される
    - LLMによる意思決定：エージェントの行動は、軽量ローカルLLMが状況と自身の性格に基づき、
    動的に生成された文法（GBNF）に従って決定する

## Worldクラスの要件
状態管理とルールの適用の全責任を負う
- プロパティ
    - location：全てのLocationNodeオブジェクトを格納する辞書。キーは場所名
    - objects：全てのObjectオブジェクトを格納する辞書。キーはオブジェクト名
    - agents：全てのAgentオブジェクトを格納する辞書。キーはエージェント名
    - agent_states：全てのエージェントの動的な状態を管理する辞書。キーはエージェント名
    - time：シミュレーション内の現在時刻を管理する。
- メソッド
    - add_agent(agent, start_location)：エージェントを追加する
    - tick（minutes: int）：時間を進める
    - get_agent_context(agent_name: str) -> dict：指定されたエージェントの現在の状態を返す
    - get_valid_actions(agent_name: str) -> list：指定されたエージェントが実行可能な行動のリストをを返す
    - execute_action(agent_name: str, action: str, target: str) -> str：指定された行動を実行し、行動の結果を説明する文字列を返す

## Agentクラスの要件
自律的な行動主体
- プロパティ
    - name：エージェントの固有名
    - personality：エージェントの性格や背景を記述したテキスト
    - memory：経験したことを時系列で記録するリスト
- メソッド
    - observe(observation_text: str): 新しい出来事をmemory_streamに記録する。
    - decide_next_action(context: dict, grammar: str) -> tuple:
    1. GameWorldから受け取ったcontextと自身のpersonality、最近の記憶を使ってプロンプトを生成する。
    2. 動的に生成されたgrammar（GBNF形式）を制約としてLLMを呼び出す。
    3. LLMの出力をパースし、行動とターゲットのタプル (action, target) を返す。

## データモデルの定義
Pydanticを使用して、world.jsonの構造を定義
- ActionType: Literalを使い、システムが認識できる全行動タイプを列挙する
- GameObject(BaseModel): オブジェクトの定義。name, description, portable (持ち運び可能か), actions (そのオブジェクトに可能な行動リスト) を含む
- LocationNode(BaseModel): 場所の定義。name, description, objects (初期配置オブジェクト名のリスト), base_actions (その場所で可能な基本行動), connections (接続している場所名のリスト) を含む
- WorldDefinition(BaseModel): world.json全体の構造。locationsのリストとobjectsのリストを含む。
