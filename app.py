import streamlit as st
import random
from datetime import datetime
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class SRKTweetGenerator:
    def __init__(self):
        # Initialize templates
        self.templates = {
            'fan_engagement': [
                "Mere pyaare {fan_term}, {gratitude_msg}. {emoji} #{hashtag}",
                "Your love {love_action}. {time_reference} {gratitude_msg}. {emoji} #{hashtag}",
                "{question_prompt} {answer_msg} {emoji} #{hashtag}",
                "To all my {fan_term}, {inspiration_msg} {emoji} #{hashtag}",
                "Just finished {activity} and thinking about {fan_thought} {emoji} #{hashtag}"
            ],
            'film_promotion': [
                "{film_element}. And yes, {promo_msg}. {anticipation_msg} {emoji} #{hashtag}",
                "{behind_scenes_msg} {progress_msg} {emoji} #{hashtag}",
                "{years_msg} {special_msg} #{hashtag}",
                "On set today: {set_description}. {emotion} {emoji} #{hashtag}"
            ],
            'philanthropy': [
                "Together we can make a difference. {cause_msg} {emoji} #{hashtag}",
                "{education_msg} Every dream matters. {emoji} #{hashtag}",
                "Your support helps us reach more people. {initiative_msg} #{hashtag}"
            ],
            'personal_update': [
                "{activity} with family is always special. {emoji} #{hashtag}",
                "Grateful for another beautiful day of {routine}. {emoji} #{hashtag}",
                "Your messages make every {time_of_day} special. {emoji} #{hashtag}"
            ]
        }
        
        self.content = {
            'fan_term': ['beautiful souls', 'SRKians', 'loved ones', 'incredible family'],
            'gratitude_msg': ['your love keeps me going', 'grateful for your endless support', 'you make everything worthwhile'],
            'emoji': ['❤️', '🙏', '✨', '💫', '🎬', '🌟'],
            'hashtag': ['SRKians', 'LifeOfSRK', 'SRKMovie', 'Bollywood'],
            'love_action': ['keeps me inspired', 'makes every day special', 'drives me to do better'],
            'time_reference': ['Even at 3 AM', 'Through every moment', 'Day after day'],
            'activity': ['shooting', 'reading scripts', 'meeting fans', 'working out'],
            'routine': ['filming', 'fan meetings', 'family time', 'script reading'],
            'time_of_day': ['morning', 'evening', 'day', 'moment'],
            'film_element': ['Action packed', 'Heart touching', 'Something special', 'A new journey'],
            'promo_msg': ['you won\'t believe what\'s coming', 'this one\'s for you', 'get ready'],
            'anticipation_msg': ['Can\'t wait to share this', 'You\'ll love this one', 'Almost there'],
            'behind_scenes_msg': ['Working hard', 'Creating magic', 'Another day of shooting'],
            'progress_msg': ['everything is looking perfect', 'the team is giving their best', 'your wait will be worth it'],
            'set_description': ['amazing stunts', 'emotional scene', 'fun moments with the team'],
            'emotion': ['feeling blessed', 'excited to share', 'grateful for this journey'],
            'question_prompt': ['Want to know my secret?', 'What keeps me going?', 'Know what I love most?'],
            'answer_msg': ['It\'s all because of you', 'Your smile is my motivation', 'The love we share'],
            'fan_thought': ['your amazing support', 'our beautiful journey together', 'the love you share'],
            'years_msg': ['25 years of magic', 'Another milestone together', 'This journey continues'],
            'special_msg': ['thanks for being part of this story', 'your love makes it all worth it'],
            'cause_msg': ['Let\'s build a better tomorrow', 'Education empowers everyone', 'Small steps, big change'],
            'education_msg': ['Knowledge opens doors.', 'Learning never stops.', 'Education transforms lives.'],
            'initiative_msg': ['Join us in making dreams come true', 'Together we can achieve more', 'Your support creates change']
        }

        # LLM Prompts
        self.llm_prompts = {
            'fan_engagement': """Generate a tweet in Shah Rukh Khan's style expressing gratitude to fans. 
            Characteristics:
            - Warm and personal tone
            - Use of endearing terms
            - Mix of English and occasional Hindi words
            - Include emojis
            - End with relevant hashtags
            - Maximum 280 characters
            Example: "My beautiful fans, your love keeps me going. Dil se shukriya for always being there. ❤️ #SRKians"
            """,
            
            'film_promotion': """Generate a tweet in Shah Rukh Khan's style promoting a film. 
            Characteristics:
            - Exciting and anticipatory tone
            - Hint at something special
            - Personal connection with audience
            - Include emojis
            - End with relevant hashtags
            - Maximum 280 characters
            Example: "Something special is coming your way. The team has poured their heart into this one. Can't wait to share this journey with you all! 🎬 #SRKMovie"
            """,
            
            'philanthropy': """Generate a tweet in Shah Rukh Khan's style about philanthropy or social causes. 
            Characteristics:
            - Inspiring and thoughtful tone
            - Focus on making a difference
            - Call for collective action
            - Include emojis
            - End with relevant hashtags
            - Maximum 280 characters
            Example: "Education can change lives. Together, we can make sure every child gets this opportunity. Join us in this journey. 📚 #SRKFoundation"
            """,
            
            'personal_update': """Generate a tweet in Shah Rukh Khan's style sharing a personal update. 
            Characteristics:
            - Casual and reflective tone
            - Share glimpse of daily life
            - Connect with fans personally
            - Include emojis
            - End with relevant hashtags
            - Maximum 280 characters
            Example: "3 AM wrap, but your messages make every moment worth it. Keep spreading love, keep shining bright. ✨ #LifeOfSRK"
            """
        }

    def generate_llm_tweet(self, category):
        """Generate tweet using GPT model"""
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are Shah Rukh Khan, the Bollywood superstar known for your wit, 
                    charm, and deep connection with fans. Generate tweets in your signature style."""},
                    {"role": "user", "content": self.llm_prompts[category]}
                ],
                max_tokens=100,
                temperature=0.8
            )

            tweet = response.choices[0].message.content.strip().replace('"', '')
            
            return {
                'success': True,
                'tweet': self._format_tweet(tweet),
                'category': category,
                'char_count': len(tweet),
                'source': 'llm'
            }
        except Exception as e:
            print(f"LLM Error: {str(e)}")
            return self.generate_template_tweet(category)

    def generate_template_tweet(self, category=None):
        """Generate tweet using templates"""
        try:
            if category is None:
                category = random.choice(list(self.templates.keys()))
            
            template = random.choice(self.templates[category])
            tweet = template
            
            for key in self.content:
                if f'{{{key}}}' in tweet:
                    tweet = tweet.replace(f'{{{key}}}', random.choice(self.content[key]))
            
            return {
                'success': True,
                'tweet': self._format_tweet(tweet),
                'category': category,
                'char_count': len(tweet),
                'source': 'template'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def generate_tweet(self, category=None, use_llm=True):
        """Generate tweet using LLM or fallback to templates"""
        if use_llm and os.getenv('OPENAI_API_KEY'):
            try:
                return self.generate_llm_tweet(category)
            except:
                return self.generate_template_tweet(category)
        return self.generate_template_tweet(category)

    def _format_tweet(self, tweet):
        """Format the tweet and ensure it meets Twitter's requirements"""
        tweet = ' '.join(tweet.split())
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
        return tweet

def main():
    st.set_page_config(
        page_title="SRK Tweet Generator",
        page_icon="🎬",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .main {
            color: white;
        }
        .stButton > button {
            width: 100%;
            background-color: #1DA1F2 !important;
            color: white !important;
            border: none !important;
            padding: 0.5rem !important;
            border-radius: 5px !important;
            font-weight: bold !important;
        }
        .tweet-box {
            padding: 1.5rem;
            border: 1px solid #1DA1F2;
            border-radius: 10px;
            margin: 1rem 0;
            background-color: #192734;
            color: white;
            font-size: 18px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .char-count {
            color: #8899A6;
            font-size: 14px;
            margin-top: 10px;
        }
        .source-tag {
            color: #1DA1F2;
            font-size: 12px;
            margin-top: 5px;
            font-style: italic;
        }
        .success-message {
            padding: 0.5rem;
            border-radius: 5px;
            margin: 1rem 0;
            background-color: #192734;
            color: #17BF63;
        }
        .history-item {
            background-color: #192734;
            padding: 1rem;
            border-radius: 5px;
            margin: 0.5rem 0;
            border-left: 3px solid #1DA1F2;
        }
        h1, h2, h3, p {
            color: white !important;
        }
        .stMarkdown {
            color: white;
        }
        .stSelectbox > div > div {
            background-color: #192734 !important;
            color: white !important;
        }
        .tweet-number {
            color: #1DA1F2;
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 8px;
        }
        footer {
            visibility: hidden;
        }
        </style>
    """, unsafe_allow_html=True)

    # App Header
    st.title("🎭 SRK Tweet Generator")
    st.markdown("Generate tweets in Shah Rukh Khan's signature style")

    # Initialize generator
    generator = SRKTweetGenerator()

    # Sidebar
    st.sidebar.header("Tweet Settings")
    
    # LLM toggle
    use_llm = st.sidebar.checkbox("Use AI for tweet generation", value=True)
    if use_llm and not os.getenv('OPENAI_API_KEY'):
        st.sidebar.warning("⚠️ OpenAI API key not found. Using template-based generation.")
        use_llm = False

    category = st.sidebar.selectbox(
        "Select Tweet Category",
        options=['fan_engagement', 'film_promotion', 'philanthropy', 'personal_update'],
        format_func=lambda x: x.replace('_', ' ').title()
    )

    # Number of tweets selector
    num_tweets = st.sidebar.number_input("Number of tweets to generate", min_value=1, max_value=20, value=5)

    # Main content
    if st.button(f"Generate {num_tweets} Tweets"):
        tweets = []
        with st.spinner('Generating tweets...'):
            for _ in range(num_tweets):
                result = generator.generate_tweet(category, use_llm=use_llm)
                if result['success']:
                    tweets.append(result)

        # Store in session state
        st.session_state['current_tweets'] = tweets

        # Display tweets
        st.markdown("### Choose your favorite tweet:")
        
        for i, tweet_result in enumerate(tweets, 1):
            tweet = tweet_result['tweet']
            source = tweet_result.get('source', 'template')
            
            st.markdown(f"""
                <div class="tweet-box">
                    <div class="tweet-number">Tweet Option #{i}</div>
                    <p style="margin-bottom: 10px;">{tweet}</p>
                    <div class="char-count">Characters: {len(tweet)}/280</div>
                    <div class="source-tag">Generated by: {source.upper()}</div>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Copy Tweet #{i}", key=f"copy_{i}"):
                    st.code(tweet)
                    st.success(f"Tweet #{i} copied to clipboard!")
            
            with col2:
                if st.button(f"Save to History #{i}", key=f"save_{i}"):
                    if 'tweet_history' not in st.session_state:
                        st.session_state['tweet_history'] = []
                    
                    st.session_state['tweet_history'].append({
                        'tweet': tweet,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'category': category,
                        'source': source
                    })
                    st.success(f"Tweet #{i} saved to history!")

    # Display history
    if 'tweet_history' in st.session_state and st.session_state['tweet_history']:
        st.sidebar.header("Recent Tweets")
        for tweet in reversed(st.session_state['tweet_history'][-5:]):
            st.sidebar.markdown(f"""
                <div class="history-item">
                    <small>{tweet['timestamp']}</small><br>
                    <small>{tweet['category'].replace('_', ' ').title()} ({tweet['source'].upper()})</small><br>
                    <p>{tweet['tweet'][:50]}...</p>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()