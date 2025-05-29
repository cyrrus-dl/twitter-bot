# Twitter Bot

A comprehensive Twitter bot that helps you manage your Twitter account. The project starts with automatic tweet deletion functionality and will progressively add more features, including advanced AI capabilities.

## Current Features

- Automatic deletion of oldest tweets
- Tracking of deleted tweets to avoid duplicates
- Respect for Twitter API rate limits
- Colorful console output for better visibility
- Caching of fetched tweets for better performance

## Planned Features

### Tweet Management
- [ ] Like and retweet management
- [ ] Tweet scheduling
- [ ] Statistics analysis
- [ ] List management
- [ ] Mention interactions
- [ ] Automatic tweet filtering

### AI Features
- [ ] Automatic tweet generation with GPT
- [ ] Tweet sentiment analysis
- [ ] Automatic inappropriate content detection
- [ ] Relevant hashtag suggestions
- [ ] Personalized automatic responses
- [ ] Trend analysis and content recommendations
- [ ] Automatic tweet categorization

## Prerequisites

- Python 3.6 or higher
- Twitter Developer Account with API access
- Twitter API v2 credentials
- OpenAI API key (for GPT features)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/twitter-bot.git
cd twitter-bot
```

2. Install required dependencies:
```bash
pip install requests requests-oauthlib python-dotenv openai transformers torch pandas numpy scikit-learn
```

3. Create a `.env` file in the root directory with your credentials:
```env
# Twitter API
API_KEY=your_api_key
API_SECRET=your_api_secret
ACCESS_TOKEN=your_access_token
ACCESS_TOKEN_SECRET=your_access_token_secret

# OpenAI API
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Tweet Deletion
```bash
python delete_tweets.py
```

### AI Tweet Generation (coming soon)
```bash
python generate_tweets.py
```

### Sentiment Analysis (coming soon)
```bash
python analyze_sentiment.py
```

## Configuration

The script contains several constants that can be modified in `delete_tweets.py`:

- `MAX_DELETIONS`: Maximum number of tweets to delete per run (default: 17)
- `DELETED_FILE`: File to store deleted tweet IDs (default: "deleted_tweets.json")
- `FETCHED_TWEETS_FILE`: File to cache fetched tweets (default: "fetched_tweets.json")

## AI Architecture

The bot will use several AI models:
- GPT for content generation
- BERT for sentiment analysis
- Classification models for categorization
- Inappropriate content detection models

## Notes

- The script includes a 1-second delay between deletions to respect Twitter's rate limits
- Deleted tweets are tracked to prevent attempting to delete the same tweet twice
- The script uses Twitter API v2, which requires elevated access
- AI features will require a valid OpenAI API key

## Error Handling

The script includes comprehensive error handling for:
- Missing environment variables
- API authentication issues
- Network errors
- Rate limiting
- AI generation errors
- Classification issues

## Contributing

Contributions are welcome! Feel free to:
1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.