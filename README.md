# Twitter Bot

A comprehensive Twitter bot that helps you manage your Twitter account. The project starts with automatic tweet deletion functionality and will progressively add more features, including advanced AI capabilities.

## Project Status

### Completed
#### Core Features
- [x] Basic project setup
- [x] Documentation (README and LICENSE)
- [x] Environment configuration

#### Tweet Management
- [x] Tweet deletion functionality
- [x] Deleted tweets tracking system
- [x] Rate limiting implementation
- [x] Error handling system

### In Progress
#### AI Integration
- [ ] AI features implementation
- [ ] Model integration setup

#### Enhanced Features
- [ ] Additional tweet management features
- [ ] User interaction features

## Current Features

### Core Functionality
- [x] Automatic deletion of oldest tweets
- [x] Tracking of deleted tweets to avoid duplicates
- [x] Respect for Twitter API rate limits

### User Interface
- [x] Colorful console output for better visibility
- [x] Progress tracking and status updates

### Data Management
- [x] Caching of fetched tweets for better performance
- [x] JSON-based storage system

## Planned Features

### Tweet Management
#### Basic Operations
- [ ] Like and retweet management
- [ ] Tweet scheduling
- [ ] List management

#### Analytics
- [ ] Statistics analysis
- [ ] Engagement metrics
- [ ] Performance tracking

#### Interaction
- [ ] Mention interactions
- [ ] Direct message handling
- [ ] Follower management

### AI Features
#### Content Generation
- [ ] Automatic tweet generation with GPT
- [ ] Content optimization
- [ ] Hashtag suggestions

#### Analysis
- [ ] Tweet sentiment analysis
- [ ] Trend analysis
- [ ] Content recommendations

#### Moderation
- [ ] Automatic inappropriate content detection
- [ ] Spam detection
- [ ] Content filtering

#### Automation
- [ ] Personalized automatic responses
- [ ] Smart scheduling
- [ ] Automatic tweet categorization

## Prerequisites

### Development Environment
- Python 3.6 or higher
- Git

### API Access
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

### Core Operations
#### Tweet Deletion
```bash
python delete_tweets.py
```

### AI Features (coming soon)
#### Tweet Generation
```bash
python generate_tweets.py
```

#### Analysis
```bash
python analyze_sentiment.py
```

## Configuration

### Core Settings
The script contains several constants that can be modified in `delete_tweets.py`:

- `MAX_DELETIONS`: Maximum number of tweets to delete per run (default: 17)
- `DELETED_FILE`: File to store deleted tweet IDs (default: "deleted_tweets.json")
- `FETCHED_TWEETS_FILE`: File to cache fetched tweets (default: "fetched_tweets.json")

## AI Architecture

### Models
The bot will use several AI models:
- GPT for content generation
- BERT for sentiment analysis
- Classification models for categorization
- Inappropriate content detection models

## Notes

### Performance
- The script includes a 1-second delay between deletions to respect Twitter's rate limits
- Deleted tweets are tracked to prevent attempting to delete the same tweet twice

### Requirements
- The script uses Twitter API v2, which requires elevated access
- AI features will require a valid OpenAI API key

## Error Handling

### API Related
- Missing environment variables
- API authentication issues
- Rate limiting

### System Related
- Network errors
- File system errors

### AI Related
- AI generation errors
- Classification issues
- Model loading errors

## Contributing

### How to Contribute
1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.