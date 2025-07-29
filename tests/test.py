from lib.controllers.memory_controller import MemoryController
from lib.utils.model_loader import ModelLoader
# from lib.models.config import reasoning
import time

def test_conversational_memory():
    """
    Test conversational memory capability with multi-turn conversation
    """
    print("=" * 60)
    print("CONVERSATIONAL MEMORY TEST")
    print("=" * 60)
    
    # Initialize components
    memory_controller = MemoryController()
    model_loader = ModelLoader(memory_controller=memory_controller)
    
    # Test session ID
    tid = "test_session_123"
    
    # Conversation scenarios to test memory
    conversation_turns = [
        {
            "user": "Hello, my name is Alex and I'm a software developer.",
            "expected_memory": "Should remember the name Alex and profession"
        },
        {
            "user": "What's my name?",
            "expected_memory": "Should recall the name Alex from previous message"
        },
        {
            "user": "I'm working on a Python project about AI. Can you help?",
            "expected_memory": "Should remember Alex is a developer and now knows about Python/AI project"
        },
        {
            "user": "What was I asking for help with?",
            "expected_memory": "Should recall the Python AI project from previous turn"
        },
        {
            "user": "My favorite color is blue. I also have a cat named Whiskers.",
            "expected_memory": "Should add new personal information to existing memory"
        },
        {
            "user": "Tell me everything you remember about me.",
            "expected_memory": "Should recall: name (Alex), profession (developer), project (Python AI), color (blue), pet (cat Whiskers)"
        }
    ]
    
    print(f"Starting conversation with thread ID: {tid}")
    print("-" * 60)
    
    # Track conversation history for verification
    conversation_history = []
    
    for i, turn in enumerate(conversation_turns, 1):
        print(f"\n🔹 TURN {i}")
        print(f"Expected Memory Test: {turn['expected_memory']}")
        print(f"User: {turn['user']}")
        
        # Create message
        user_message = {"role": "user", "content": turn['user']}
        
        # Add to history
        conversation_history.append(user_message)
        
        try:
            # Get response from model with memory
            start_time = time.time()
            response = model_loader.chat(tid, messages=[user_message])
            end_time = time.time()
            
            print(f"Assistant: {response}")
            print(f"Response time: {end_time - start_time:.2f}s")
            
            # Add assistant response to history
            if isinstance(response, str):
                conversation_history.append({"role": "assistant", "content": response})
            
        except Exception as e:
            print(f"❌ Error during turn {i}: {str(e)}")
            print(f"Exception type: {type(e).__name__}")
            break
        
        print("-" * 40)
        
        # Small delay between turns to simulate natural conversation
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print("MEMORY TEST SUMMARY")
    print("=" * 60)
    print(f"Total turns completed: {i}")
    print(f"Thread ID used: {tid}")
    print(f"Conversation history length: {len(conversation_history)}")
    
    # Test memory persistence by starting a new conversation in same thread
    print("\n🔹 MEMORY PERSISTENCE TEST")
    print("Starting new conversation in same thread to test memory persistence...")
    
    try:
        persistence_message = {"role": "user", "content": "Hi again! Do you remember our previous conversation?"}
        persistence_response = model_loader.chat(tid, messages=[persistence_message])
        print(f"User: {persistence_message['content']}")
        print(f"Assistant: {persistence_response}")
        
        if any(keyword in str(persistence_response).lower() for keyword in ['alex', 'developer', 'python', 'blue', 'whiskers']):
            print("✅ Memory persistence: PASSED - Assistant remembers previous conversation")
        else:
            print("❌ Memory persistence: FAILED - Assistant doesn't remember previous conversation")
            
    except Exception as e:
        print(f"❌ Memory persistence test failed: {str(e)}")
    
    # Test with different thread ID (should not remember)
    print("\n🔹 THREAD ISOLATION TEST")
    print("Testing with different thread ID (should not remember previous conversation)...")
    
    try:
        new_tid = "different_session_456"
        isolation_message = {"role": "user", "content": "What's my name and what do you know about me?"}
        isolation_response = model_loader.chat(new_tid, messages=[isolation_message])
        print(f"User (new thread {new_tid}): {isolation_message['content']}")
        print(f"Assistant: {isolation_response}")
        
        if not any(keyword in str(isolation_response).lower() for keyword in ['alex', 'developer', 'python', 'blue', 'whiskers']):
            print("✅ Thread isolation: PASSED - Assistant doesn't remember other thread's conversation")
        else:
            print("❌ Thread isolation: FAILED - Assistant remembers other thread's conversation")
            
    except Exception as e:
        print(f"❌ Thread isolation test failed: {str(e)}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_conversational_memory()