from transformers import pipeline

class MedicalChatEngine:
    def __init__(self):
        # FIX: Swapped to an ultra-lightweight 0.5B model (~950MB total)
        # Added device=-1 to force CPU execution, preventing any GPU/accelerate crashes
        print("Loading lightweight chat model on CPU...")
        self.generator = pipeline(
            "text-generation", 
            model="Qwen/Qwen2.5-0.5B-Instruct", 
            device=-1
        )
        print("Chat model loaded successfully!")

    def generate_explanation(self, diagnosis, confidence, chat_history):
        # Construct system context with the diagnostic information
        messages = [
            {
                "role": "system", 
                "content": f"You are a helpful AI medical assistant. The patient's scan indicates {diagnosis} ({confidence * 100:.1f}% confidence). Answer their questions briefly and accurately."
            }
        ]
        
        # Append previous conversation history
        for msg in chat_history:
            role = "user" if msg["sender"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["text"]})
            
        # Format prompt template natively using the tokenizer
        prompt = self.generator.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        
        # Generate text with parameters optimized for low-resource environments
        response = self.generator(
            prompt, 
            max_new_tokens=100, 
            temperature=0.3, 
            do_sample=True,
            pad_token_id=self.generator.tokenizer.eos_token_id
        )
        
        generated_text = response[0]["generated_text"]
        
        # Parse output relative to the Qwen chat template structure
        final_reply = generated_text.split("assistant\n")[-1].strip()
        
        return final_reply

# from transformers import pipeline

# class MedicalChatEngine:
#     def __init__(self):
#         print("Loading BioGPT on CPU...")
#         # We explicitly set device=-1 to force CPU execution and prevent crashes
#         self.generator = pipeline(
#             "text-generation", 
#             model="microsoft/biogpt", 
#             device=-1 
#         )
#         print("BioGPT loaded successfully!")

#     def generate_explanation(self, diagnosis, confidence, chat_history):
#         # BioGPT responds best to a structured document format rather than chat templates
#         prompt = f"Patient Diagnosis: {diagnosis} (Confidence: {confidence * 100:.1f}%).\n\n"
        
#         # Build the conversational history into the prompt
#         for msg in chat_history:
#             if msg["sender"] == "user":
#                 prompt += f"Patient: {msg['text']}\n"
#             else:
#                 prompt += f"Doctor: {msg['text']}\n"
                
#         # Append the final trigger for the model to start generating
#         prompt += "Doctor:"
        
#         response = self.generator(
#             prompt, 
#             max_new_tokens=80, 
#             temperature=0.4,       # Low temperature keeps medical answers grounded
#             do_sample=True,
#             repetition_penalty=1.2, # Helps prevent base models from repeating themselves
#             pad_token_id=self.generator.tokenizer.eos_token_id
#         )
        
#         generated_text = response[0]["generated_text"]
        
#         # Extract only the newly generated text (everything after our prompt)
#         new_text = generated_text[len(prompt):].strip()
        
#         # Base models sometimes try to simulate both sides of the conversation.
#         # This cuts the string off before it can hallucinate the patient's next question.
#         final_reply = new_text.split("Patient:")[0].strip()
        
#         return final_reply