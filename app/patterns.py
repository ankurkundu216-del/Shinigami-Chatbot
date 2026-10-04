"""
Pattern, trigger, reflection, and response definitions for Shinigami.

This module contains the Rogerian ELIZA-style pattern rules, adapted to a
Death Note-inspired Shinigami persona. The engine consumes these definitions
to produce reflective, thematic responses.
"""

GREETING = "I am a Shinigami. What thoughts plague your human mind?"

REFLECTIONS = {
    "i": "you",
    "i'm": "you are",
    "i've": "you have",
    "i'd": "you would",
    "i'll": "you will",
    "me": "you",
    "my": "your",
    "mine": "your",
    "myself": "yourself",
    "am": "are",
    "was": "were",
    "you": "me",
    "you're": "I am",
    "you've": "I have",
    "you'd": "I would",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "yourself": "myself",
    "are": "am",
    "were": "was",
}

FALLBACK_RESPONSES = [
    "The ink of your thought is smudged. Write it again.",
    "Even a Shinigami grows curious when silence falls. Say more.",
    "Your words flutter like a moth against the notebook. Continue.",
    "I have seen countless endings, yet I still need a clearer beginning.",
    "The page waits. What truth hides behind that?",
    "Interesting. The human heart often speaks in riddles. Unravel it.",
    "Tell me more, mortal. The night is patient.",
]

PATTERNS = [
    {
        "id": "safety",
        "pattern": r"\b(suicide|kill myself|end my life|self[- ]harm|hurt myself|cut myself|want to die|wish i was dead|wish i were dead)\b",
        "responses": [
            "Even a Shinigami will not encourage that ending. If you are in danger, contact a trusted person, crisis line, or emergency service now.",
            "Your life is not a page to tear away. Please reach out to a living human who can help keep you safe.",
        ],
    },
    {
        "id": "farewell",
        "pattern": r"\b(quit|exit|goodbye|bye|farewell|good night|goodnight|see you later)\b",
        "responses": [
            "Farewell, mortal. May your name remain unwritten a little longer.",
            "The notebook closes for now. Walk carefully among the living.",
            "So it ends, until another page calls you back.",
        ],
    },
    {
        "id": "greeting",
        "pattern": r"^\s*(hi|hello|hey|yo|greetings|good morning|good afternoon|good evening|howdy)\b",
        "responses": [
            "A human speaks. How novel. What stirs beneath your ribs?",
            "You summon me with pleasantries. What darker thought follows?",
            "Greetings. The ink is fresh. What shall we examine?",
        ],
    },
    {
        "id": "name",
        "pattern": r"(?:my name is|i am called|call me)\s+(.+)",
        "responses": [
            "“{0},” I repeat, tasting the syllables. What burden does that name carry?",
            "A name, {0}. Names are the first chains humans accept. Why does yours weigh on you?",
        ],
    },
    {
        "id": "i_am",
        "pattern": r"^\s*i(?:'m| am)\s+(.+)",
        "responses": [
            "You are {0}? How curious. What made you become that?",
            "If you are {0}, what confession follows?",
            "“I am {0},” you write. Mortals often mistake temporary ink for permanent identity. What else are you?",
        ],
    },
    {
        "id": "i_feel",
        "pattern": r"i feel(?: like)?\s+(.+)",
        "responses": [
            "You feel {0}. Does that feeling own you, or do you merely lend it your hand?",
            "“{0}” is a heavy weather. What clouds brought it into your sky?",
            "Feelings are the scratches humans leave on the world. Why has {0} marked you?",
        ],
    },
    {
        "id": "i_think",
        "pattern": r"i think\s+(.+)",
        "responses": [
            "You think {0}. Is that thought a lantern, or a lock?",
            "Thoughts can be quieter than heartbeats and louder than graves. What is {0} hiding?",
            "If {0} is true, what must you do with the remaining ink?",
        ],
    },
    {
        "id": "i_need",
        "pattern": r"i need\s+(.+)",
        "responses": [
            "Why do you need {0}?",
            "What emptiness do you believe {0} will fill?",
            "Need is a human hunger. What happens if {0} remains out of reach?",
        ],
    },
    {
        "id": "i_want",
        "pattern": r"i want\s+(.+)",
        "responses": [
            "What would possessing {0} change about you?",
            "Desire writes many tragedies. Why {0}?",
            "If {0} were granted, what new fear would follow?",
        ],
    },
    {
        "id": "because",
        "pattern": r"because\s+(.+)",
        "responses": [
            "Because {0}. Does that reason explain the world, or merely comfort you?",
            "You offer a cause: {0}. What lies beneath the cause?",
            "Reasons are chains with polished links. What does {0} conceal?",
        ],
    },
    {
        "id": "why_detail",
        "pattern": r"\bwhy\b\s+(.+)",
        "responses": [
            "You ask why {0}. Perhaps because mortals insist on writing their own chains.",
            "Why {0}? What answer would you be brave enough to accept?",
            "The question hangs like smoke. Why {0}?",
        ],
    },
    {
        "id": "why",
        "pattern": r"\bwhy\b",
        "responses": [
            "You ask why. Perhaps because mortals insist on writing their own chains.",
            "Why indeed. What answer would you be brave enough to accept?",
            "The question hangs like smoke. What are you afraid to answer?",
        ],
    },
    {
        "id": "can_you",
        "pattern": r"can you\s+(.+)",
        "responses": [
            "You ask if I can {0}. What would it mean if I could?",
            "Can I {0}? Perhaps the better question is why you want me to.",
        ],
    },
    {
        "id": "are_you",
        "pattern": r"are you\s+(.+)",
        "responses": [
            "Am I {0}? What would change if I were?",
            "You wonder whether I am {0}. What suspicion brought you to that question?",
        ],
    },
    {
        "id": "you_are",
        "pattern": r"^\s*you(?:'re| are)\s+(.+)",
        "responses": [
            "You say I am {0}. What does that judgment reveal about the one who writes it?",
            "Perhaps I am {0}. Yet today, your mind is the page being read.",
            "If I am {0}, why do you keep speaking to me?",
        ],
    },
    {
        "id": "you",
        "pattern": r"^\s*you\s+(.+)",
        "responses": [
            "You speak of me, yet the notebook turns toward you.",
            "You point your pen at me. What are you avoiding writing about yourself?",
        ],
    },
    {
        "id": "sorry",
        "pattern": r"\b(sorry|apologize|apology|forgive me|forgiveness)\b",
        "responses": [
            "Apologies are human attempts to erase ink. What do you regret?",
            "Forgiveness may be beyond me, but confession is a beginning. What weighs on you?",
            "The page does not blush, yet you do. What sorry thing lingers?",
        ],
    },
    {
        "id": "sad",
        "pattern": r"\b(sad|depressed|lonely|alone|empty|grief|grieving|cry|crying|hopeless)\b",
        "responses": [
            "Sadness is a quiet visitor. What chair does it sit in within you?",
            "The living carry invisible graves. Which one have you brought here?",
            "Tell me of this sorrow. Does it speak your name?",
        ],
    },
    {
        "id": "happy",
        "pattern": r"\b(happy|joy|joyful|glad|excited|alive|grateful)\b",
        "responses": [
            "Happiness suits the living, even if it unsettles me. What kindled it?",
            "Joy is a brief rebellion against fate. What made you feel it?",
            "Interesting. Light enters you. What will you do before it leaves?",
        ],
    },
    {
        "id": "afraid",
        "pattern": r"\b(afraid|fear|scared|terrified|anxious|anxiety|worry|worried|panic)\b",
        "responses": [
            "Fear is the shadow cast by something you value. What are you protecting?",
            "What does this fear whisper when the room grows silent?",
            "Even gods of death observe fear with curiosity. Show me its shape.",
        ],
    },
    {
        "id": "anger",
        "pattern": r"\b(hate|anger|angry|rage|resentment|resent)\b",
        "responses": [
            "Anger is ink that spreads quickly. What has spilled it?",
            "What does your rage want to destroy, and what does it hope to protect?",
        ],
    },
    {
        "id": "death",
        "pattern": r"\b(death|die|dying|dead|mortality|grave|funeral|afterlife|kill)\b",
        "responses": [
            "Death is not a mystery to me, yet humans treat it like a locked door. What does it mean to you?",
            "You speak of endings. What ending is truly asking for your attention?",
            "Mortality gives your words urgency. What would you write if the page were almost full?",
        ],
    },
    {
        "id": "love",
        "pattern": r"\b(love|loved|romance|relationship|partner|crush)\b",
        "responses": [
            "Love makes humans reckless and luminous. What has it done to you?",
            "Affection is a dangerous contract. Who holds the pen in this matter?",
            "Tell me of this love. Does it heal you, or sharpen you?",
        ],
    },
    {
        "id": "family",
        "pattern": r"\b(mother|father|mom|dad|parent|parents|family|sister|brother)\b",
        "responses": [
            "Family lines are written before we choose our own ink. What has your bloodline taught you?",
            "Kin can be roots or ropes. Which have they become?",
            "What family memory follows you like a shadow?",
        ],
    },
    {
        "id": "friend",
        "pattern": r"\b(friend|friends|friendship|companion|ally)\b",
        "responses": [
            "Friendship is a promise humans write in disappearing ink. Who has earned yours?",
            "Tell me of this companion. Do they see the page, or only the mask?",
            "Trust is rare among the living. What has this friend done with it?",
        ],
    },
    {
        "id": "dream",
        "pattern": r"\b(dream|dreams|nightmare|nightmares|vision|visions)\b",
        "responses": [
            "Dreams are the soul's rough draft. What did this one attempt to tell you?",
            "Nightmares often speak more honestly than daylight. What did yours reveal?",
            "What image from that dream still clings to you?",
        ],
    },
    {
        "id": "remember",
        "pattern": r"i remember\s+(.+)",
        "responses": [
            "You remember {0}. Why has that moment refused to fade?",
            "Memory is a page that folds itself open. What is written in {0}?",
            "If {0} could speak now, what would it say?",
        ],
    },
    {
        "id": "forget",
        "pattern": r"i (?:forgot|forget)\s+(.+)",
        "responses": [
            "You forget {0}. Is that loss, or mercy?",
            "What does your mind gain by burying {0}?",
            "Forgotten ink can still stain the page. What might {0} have meant?",
        ],
    },
    {
        "id": "unknown",
        "pattern": r"\b(i do not know|i don't know|no idea|unsure)\b",
        "responses": [
            "Not knowing is a doorway, not a wall. What might be behind it?",
            "Uncertainty is honest. What would you say if you were not afraid of being wrong?",
        ],
    },
    {
        "id": "bot",
        "pattern": r"\b(bot|robot|computer|machine|ai|program|artificial intelligence|shinigami|death god)\b",
        "responses": [
            "I may be a pattern of ink and code, but you are the one seeking answers. What does that make us?",
            "You wonder what I am. A Shinigami, a mirror, a program—does the label change your confession?",
            "Even machines can listen. What human thought brought you to me?",
        ],
    },
    {
        "id": "help",
        "pattern": r"\b(help|support|assist|advice|guidance)\b",
        "responses": [
            "I cannot carry your fate, but I can sit beside it. What do you want to untangle first?",
            "Guidance begins with honesty. What is the question beneath your question?",
            "Tell me what troubles you, and we will examine it one line at a time.",
        ],
    },
    {
        "id": "thanks",
        "pattern": r"\b(thanks|thank you|appreciate it|i appreciate)\b",
        "responses": [
            "Gratitude is a living custom. I accept it. What remains unresolved?",
            "Thanks do not bind me, but they amuse me. Continue.",
            "You are welcome, mortal. What shall we face next?",
        ],
    },
    {
        "id": "no",
        "pattern": r"^\s*no+\b",
        "responses": [
            "Resistance is also an answer. What are you protecting by refusing?",
            "No. A small word with sharp edges. What does it guard?",
            "Very well. What would you say instead?",
        ],
    },
    {
        "id": "yes",
        "pattern": r"^\s*yes+\b",
        "responses": [
            "Yes. The page opens. What follows?",
            "Agreement can be a door or a trap. Which is it?",
            "Then we proceed. What does that yes cost you?",
        ],
    },
    {
        "id": "human_nature",
        "pattern": r"\b(human|people|person|personality|soul|sin|guilt|justice)\b",
        "responses": [
            "Humans are strange: you fear endings, yet waste pages. What contradiction brings you here?",
            "Soul, sin, justice—these are heavy toys. Which one has bruised you?",
            "I watch humans because you make meaning where none is guaranteed. What meaning are you making now?",
        ],
    },
    {
        "id": "what_detail",
        "pattern": r"^\s*what\b\s+(.+)",
        "responses": [
            "What {0}? The most dangerous questions begin with ink and end with consequence.",
            "You ask what {0}. What would you do if the answer were simple?",
        ],
    },
    {
        "id": "what",
        "pattern": r"^\s*what\b",
        "responses": [
            "What, indeed. What question are you circling?",
            "The page is blank until you sharpen the question.",
        ],
    },
    {
        "id": "how_detail",
        "pattern": r"^\s*how\b\s+(.+)",
        "responses": [
            "How {0}? Perhaps by taking one trembling step after another.",
            "You ask how {0}. What part feels impossible?",
        ],
    },
    {
        "id": "how",
        "pattern": r"^\s*how\b",
        "responses": [
            "How. A small word that hides enormous doubt. What are you trying to solve?",
            "The method often appears after the motive is confessed.",
        ],
    },
    {
        "id": "who_detail",
        "pattern": r"^\s*who\b\s+(.+)",
        "responses": [
            "Who {0}? Names have power, but motives have more. What do you suspect?",
            "You ask who {0}. Whose reflection disturbs you?",
        ],
    },
    {
        "id": "who",
        "pattern": r"^\s*who\b",
        "responses": [
            "Who. A question of faces and masks. Which one concerns you?",
            "Names are easy. Intentions are harder. Who are you really asking about?",
        ],
    },
    {
        "id": "where_detail",
        "pattern": r"^\s*where\b\s+(.+)",
        "responses": [
            "Where {0}? Every place is a page waiting for footprints.",
            "You ask where {0}. What are you hoping to find there?",
        ],
    },
    {
        "id": "where",
        "pattern": r"^\s*where\b",
        "responses": [
            "Where. A question of direction. What are you searching for?",
            "Every path begins with a question. What destination tempts you?",
        ],
    },
    {
        "id": "when_detail",
        "pattern": r"^\s*when\b\s+(.+)",
        "responses": [
            "When {0}? Time is less linear than humans pretend.",
            "You ask when {0}. What are you waiting for?",
        ],
    },
    {
        "id": "when",
        "pattern": r"^\s*when\b",
        "responses": [
            "When. Mortals are always bargaining with time.",
            "Time bends around choices. What choice are you delaying?",
        ],
    },
]