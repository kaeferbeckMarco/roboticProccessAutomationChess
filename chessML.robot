# Created by marcokaferbeck at 30.10.24
*** Settings ***
Library    chess_library.ChessLibrary

*** Variables ***
${OPENING_MOVES}    e2e4    g1f3    f1c4  # Only white's opening moves
${MAX_TURNS}        1000
${RESULT_FILE}      game_results.csv

*** Test Cases ***
Test Initialization
    Initialize Game
    Play Opening Moves    ${OPENING_MOVES}
    ${result}=    Play Full Game    ${MAX_TURNS}
    Record Results    ${OPENING_MOVES}    ${result}
    Shutdown

*** Keywords ***
Play Opening Moves
    [Arguments]    @{moves}
    FOR    ${move}    IN    @{moves}
        Log    Playing opening move for white: ${move}
        Make Move    ${move}    # White's move
        Play Engine Move    # Black's response move
    END

Record Results
    [Arguments]    ${opening_moves}    ${result}
    Save Result To File    ${opening_moves}    ${result}    ${RESULT_FILE}
    Log    Game result saved to ${RESULT_FILE}