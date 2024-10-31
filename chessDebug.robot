# Created by marcokaferbeck at 29.10.24
*** Settings ***
Library    chess_library.ChessLibrary

*** Variables ***
@{OPENING_MOVES}    e2e4    e7e5    g1f3    b8c6    f1c4    f8c5
${MAX_TURNS}        1000
${RESULT_FILE}      game_results.txt

*** Test Cases ***
Test Initialization
    Initialize Game
    Play Opening Moves    ${OPENING_MOVES}
    ${result}=    Play Full Game    ${MAX_TURNS}
    Record Results    ${result}
    Shutdown

*** Keywords ***
Play Opening Moves
    [Arguments]    @{moves}
    FOR    ${move}    IN    @{moves}
        Log    Playing opening move: ${move}
        Make Move    ${move}    # Pass each move individually
    END

Record Results
    [Arguments]    ${result}
    Save Result To File    ${result}    ${RESULT_FILE}
    Log    Game result saved to ${RESULT_FILE}