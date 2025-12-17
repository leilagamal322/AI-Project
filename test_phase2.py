"""
Simple test script for Phase 2 implementation.
"""

def test_connect4_basic():
    """Test basic Connect 4 game functionality."""
    print("Testing Connect 4 basic functionality...")
    
    try:
        from env.connect4_env import Connect4Env
        
        # Create game
        game = Connect4Env()
        print("✓ Game created")
        
        # Test initial state
        assert len(game.get_valid_actions()) == 7, "Should have 7 valid columns initially"
        print("✓ Initial state correct")
        
        # Test making moves
        assert game.make_move(3), "Should be able to move in column 3"
        assert game.current_player == -1, "Should switch to player -1"
        print("✓ Move execution works")
        
        # Test undo
        assert game.undo_move(), "Should be able to undo move"
        assert game.current_player == 1, "Should restore player 1"
        assert len(game.get_valid_actions()) == 7, "Should restore valid actions"
        print("✓ Undo works")
        
        # Test winning condition
        game = Connect4Env()
        # Create a horizontal win for player 1
        for col in [0, 1, 2]:
            game.make_move(col)  # Player 1
            game.make_move(col)  # Player 2 (stack on top)
        game.make_move(3)  # Player 1 wins
        winner = game.check_winner()
        assert winner == 1, f"Player 1 should win, got {winner}"
        print("✓ Win detection works")
        
        print("\nAll basic tests passed! ✓")
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_algorithms():
    """Test Minimax and Alpha-Beta algorithms."""
    print("\nTesting adversarial search algorithms...")
    
    try:
        from env.connect4_env import Connect4Env
        from algos.adversarial_search import minimax_search, alphabeta_search
        
        game = Connect4Env()
        game.make_move(3)
        original_board = game.board.copy()
        original_player = game.current_player
        
        best_move_mm, tracker_mm = minimax_search(game, max_depth=2)
        assert best_move_mm is not None or len(game.get_valid_actions()) == 0
        assert tracker_mm.nodes_expanded > 0
        assert np.array_equal(game.board, original_board)
        assert game.current_player == original_player
        print(f"✓ Minimax works (expanded {tracker_mm.nodes_expanded} nodes)")
        
        best_move_ab, tracker_ab = alphabeta_search(game, max_depth=2)
        assert best_move_ab is not None or len(game.get_valid_actions()) == 0
        assert tracker_ab.nodes_expanded > 0
        assert tracker_ab.nodes_expanded <= tracker_mm.nodes_expanded
        assert np.array_equal(game.board, original_board)
        assert game.current_player == original_player
        print(f"✓ Alpha-Beta works (expanded {tracker_ab.nodes_expanded} nodes, pruned {tracker_ab.nodes_pruned})")
        print(f"  Efficiency: {((1 - tracker_ab.nodes_expanded/tracker_mm.nodes_expanded) * 100):.1f}% reduction")
        
        print("\nAll algorithm tests passed! ✓")
        return True
        
    except Exception as e:
        print(f"\n✗ Algorithm test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("="*60)
    print("Phase 2 Implementation Test")
    print("="*60)
    
    test1 = test_connect4_basic()
    test2 = test_algorithms()
    
    print("\n" + "="*60)
    if test1 and test2:
        print("All tests passed! ✓✓✓")
    else:
        print("Some tests failed. Please check the errors above.")
    print("="*60)

