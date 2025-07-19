# 🚀 Setup Guide: OpenRouter + Tavily Integration

## ✅ **Quick Setup (5 minutes)**

### 1. **Get API Keys**
- **OpenRouter**: https://openrouter.ai/ → Sign up → Get API key
- **Tavily**: https://tavily.com/ → Sign up → Get API key

### 2. **Create .env file**
Create a `.env` file in the `DeepWebResearcher` folder:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. **Test the Setup**
```bash
cd DeepWebResearcher
python test_openrouter.py
```

### 4. **Start the Backend**
```bash
python app.py
```

### 5. **Start the Frontend**
```bash
cd ../ChatBot
npm run dev
```

## 🔧 **Model Options & Costs**

### **OpenRouter Models (choose one):**

| Model | Quality | Cost | Use Case |
|-------|---------|------|----------|
| `anthropic/claude-3.5-sonnet` | ⭐⭐⭐⭐⭐ | High | Best quality research |
| `mistralai/mixtral-8x7b-instruct` | ⭐⭐⭐⭐⭐ | Medium | **RECOMMENDED** - Excellent quality & value |
| `openai/gpt-3.5-turbo` | ⭐⭐⭐⭐ | Medium | Good balance |
| `meta-llama/llama-3.1-8b-instruct` | ⭐⭐⭐ | Low | Budget option |

### **Change Model:**
Edit `draftagent.py` line 25-26:
```python
model="mistralai/mixtral-8x7b-instruct",  # Change this line
```

## 💰 **Credit Management**

### **If you get "402 - requires more credits" error:**

1. **Reduce max_tokens** (already done):
   - Research: 4000 tokens
   - Fact-checking: 2000 tokens

2. **Use cheaper model**:
   - Change to `openai/gpt-3.5-turbo`
   - Or `meta-llama/llama-3.1-8b-instruct`

3. **Add credits to OpenRouter**:
   - Visit https://openrouter.ai/settings/credits
   - Add payment method

## 🐛 **Troubleshooting**

### **Frontend PostCSS Error:**
```bash
cd ChatBot
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest
```

### **Backend Import Error:**
```bash
cd DeepWebResearcher
pip install -r requirements.txt
```

### **OpenRouter Connection Error:**
1. Check API key in `.env` file
2. Run `python test_openrouter.py`
3. Verify internet connection

### **Tavily Search Error:**
1. Check Tavily API key
2. Verify Tavily account is active
3. Check search quota limits

## 📊 **Performance Tips**

### **For Better Results:**
- Use `anthropic/claude-3.5-sonnet` for complex research
- Use `openai/gpt-3.5-turbo` for general tasks
- Use `meta-llama/llama-3.1-8b-instruct` for simple queries

### **For Lower Costs:**
- Reduce `max_tokens` values
- Use cheaper models
- Limit research complexity

## 🔄 **Quick Model Switch**

To quickly switch between models, edit these lines in `draftagent.py`:

```python
# For best quality (expensive):
model="anthropic/claude-3.5-sonnet"

# For excellent quality & value (RECOMMENDED):
model="mistralai/mixtral-8x7b-instruct"

# For good balance (medium cost):
model="openai/gpt-3.5-turbo"

# For budget (cheap):
model="meta-llama/llama-3.1-8b-instruct"
```

## ✅ **Verification Checklist**

- [ ] OpenRouter API key added to `.env`
- [ ] Tavily API key added to `.env`
- [ ] `python test_openrouter.py` passes
- [ ] Backend starts without errors
- [ ] Frontend loads at http://localhost:5173
- [ ] Research functionality works

## 🆘 **Need Help?**

1. **Check the logs** in your terminal
2. **Verify API keys** are correct
3. **Test with simple queries** first
4. **Check credit balance** on OpenRouter

Your application is now ready with OpenRouter + Tavily! 🎉 