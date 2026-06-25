# タスクのStatus遷移

## テスト項目
- 可能な遷移先のStatusへ遷移できるか
- 不可能な遷移先のStatusへの遷移は表示されないか

## ToDoからの遷移
- 可能な遷移先
    - in_progress
    - cancell
    - done
- 禁止
    - todo

## in_progressからの遷移
- 可能な遷移先
    - done
    - todo
    - cancelled
- 禁止
    - in_progress

## doneからの遷移
- 可能な遷移先
    - todo
- 禁止
    - done
    - in_progress
    - cancelled

## cancelledからの遷移
- 可能な遷移先
    - todo
- 禁止
    - done
    - in_progress
    - cancelled