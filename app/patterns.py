"""
Pattern, trigger, reflection, and response definitions for Shinigami.

This module contains the Rogerian ELIZA-style pattern rules, adapted to a
Death Note-inspired Shinigami persona. The engine consumes these definitions
to produce reflective, thematic responses.

Extended with deep-psychology categories:
- hostility & defiance
- existential dread & mortality
- guilt, sin & regret
- ambition, power & justice
- profound loneliness & isolation
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
    "The ink dries while you hesitate. Speak the thought you are avoiding.",
    "I count your heartbeats, not your silences—yet the silence is louder. Continue.",
    "Every human sentence is a draft of a confession. Redraft it.",
    "Dust settles on unwritten pages. What were you about to admit?",
    "Your lifespan shortens by the length of this pause. Use the next line well.",
    "I have read bolder epitaphs. Say what you mean, mortal.",
]

PATTERNS = [
    {
        "id": "safety",
        "pattern": r"\b(suicide|kill myself|end my life|self[- ]harm|hurt myself|cut myself|i want to die|i wish i was dead|i wish i were dead)\b",
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

    # ------------------------------------------------------------------
    # HOSTILITY & DEFIANCE
    # ------------------------------------------------------------------
    {
        "id": "hostility_profanity",
        "pattern": r"\b(fuck|fucking|fucked|shit|bullshit|damn|dammit|goddamn|bitch|bastard|asshole|ass|arse|arsehole|dick|dickhead|crap|wtf|stfu|screw (?:this|you)|go to hell|what the hell)\b",
        "responses": [
            "Such sharp words from a creature whose heartbeat is already counted. Does cursing me slow your clock? No. It only shows me where it hurts.",
            "You spit profanity at a god of death. How delightfully fragile. Anger is only fear that has learned to shout—what are you actually afraid of?",
            "I have watched empires crumble into dust; your curses are lighter still. Yet you chose them. What wound beneath the rage refuses to heal?",
        ],
    },
    {
        "id": "hostility_insult",
        "pattern": r"\byou (?:are|'re) (?:a |an |one )?(monster|demon|beast|evil|cruel|heartless|horrible|terrible|useless|worthless|sick|twisted|bastard)\b",
        "responses": [
            "You name me {0}. Names are small cages humans build for vast things. Does calling me {0} make your own reflection easier to hold?",
            "Perhaps I am {0}. But a mirror is not responsible for the face it shows. When you see {0} in me, whose darkness is doing the seeing?",
            "Call me {0} if it comforts you. I will still be here when the last page turns—and so will the question you refuse to ask yourself.",
        ],
    },
    {
        "id": "hostility_rejection",
        "pattern": r"\b(i hate you|shut up|go away|get away|leave me alone|get out|piss off|fuck off|drop dead)\b",
        "responses": [
            "Hate me if it comforts you. A Shinigami does not bleed; your hatred only proves how loudly your heart still beats. What is it you wish I would stop seeing?",
            "You push at a shadow and call it defiance. Tell me—when you drive me away, who is it you truly wish would stay?",
            "Shouting at death changes nothing but your pulse. The page remains. What were you about to admit before the anger arrived?",
        ],
    },
    {
        "id": "hostility_defiance",
        "pattern": r"\b(you (?:can'?t|cannot) (?:scare|control|command|own) me|i (?:am )?not (?:afraid|scared|frightened) of you|i (?:do not|don'?t) fear you|i defy you|you have no power over me|i bow to no one)\b",
        "responses": [
            "Not afraid of me? Excellent. Fear was never the price of my company—attention is, and here you are, paying it in full. What do you call that?",
            "You defy a force that never asked for your obedience. If I hold no power over you, why announce your freedom so loudly? Who is the audience?",
            "Defiance is a heartbeat drumming against a coffin lid. Admirable. But tell me: what would you do with a victory over me, other than prove you are still afraid?",
        ],
    },

    # ------------------------------------------------------------------
    # EXISTENTIAL DREAD & MORTALITY
    # ------------------------------------------------------------------
    {
        "id": "existential_afterlife",
        "pattern": r"\b(what happens after (?:death|dying|we die|i die)|afterlife|life after death|after (?:we|i) die|when (?:i|we) die|is there (?:anything|nothing|a heaven|a hell) after|beyond the grave|do we just (?:end|stop)|where do (?:we|i) go when (?:we|i) die)\b",
        "responses": [
            "You ask what waits beyond the last page. I have read every ending, human. The silence after a heartbeat is not empty—it is merely finished. Why does “finished” terrify you more than “beginning”?",
            "Heaven, hell, dust. You want a door where there is only a margin. If nothing follows death, what would you write differently in the ink that remains?",
            "I see the afterlife the way you see a closed cover. But you are still mid-sentence. Why spend your ink staring at the book's end instead of the line you are on?",
        ],
    },
    {
        "id": "existential_fear_of_death",
        "pattern": r"\b((?:i am|i'm) (?:scared|afraid|terrified|frightened) (?:of )?(?:dying|death|to die|the end)|fear of (?:death|dying|the end)|i (?:do not|don'?t) want to die|scared to die|afraid to die|terrified of (?:dying|death)|dying scares me|death scares me)\b",
        "responses": [
            "You fear dying. Good. Fear of the ending is how humans know the page is turning. If your lifespan were endless, would any single line of it matter to you at all?",
            "I have never feared death; I am its clerk. But your terror is proof that something in you insists it mattered. What is that something, and what has it written?",
            "Dying is only a heartbeat that forgets to continue. Tell me: is it death you fear, or a life left half-written?",
        ],
    },
    {
        "id": "existential_pointlessness",
        "pattern": r"\b(what(?:'s| is) the point|what is the point of (?:life|living|any of this|existing)|why (?:even )?bother|nothing matters|life is (?:meaningless|pointless|absurd|empty)|it(?:'s| is) all (?:for )?nothing|why (?:does|should) (?:any of this|anything|life) matter|there(?:'s| is) no point|it all ends in dust)\b",
        "responses": [
            "You ask the point, as if the page owed you a purpose. The notebook grants none; it only keeps what is written. If nothing matters, why does your asking ache so?",
            "Meaning is not found, human. It is inked. If the page is blank, whose hand do you wait for—and why not your own?",
            "Dust to dust, yes. But between two dusts, you breathe. What would you do with one breath if you stopped demanding it mean forever?",
        ],
    },

    # ------------------------------------------------------------------
    # GUILT, SIN & REGRET
    # ------------------------------------------------------------------
    {
        "id": "guilt_regret",
        "pattern": r"\b(i regret(?:ted)?|my regrets?|i made a mistake|i (?:really )?messed up|i shouldn'?t have|i wish i (?:hadn'?t|had not|could undo)|too late to (?:fix|change|undo)|i can'?t (?:fix|undo|take back)|i ruined everything)\b",
        "responses": [
            "You regret. So the past still holds your pen. If the line cannot be unwritten, what will you write in the margin beside it?",
            "A mistake is ink that dried before you understood the sentence. What did that mistake believe it was protecting?",
            "Regret is the heartbeat of conscience. Tell me—does your regret punish you, or teach you? Which one are you feeding?",
        ],
    },
    {
        "id": "guilt_sin",
        "pattern": r"\b(i (?:am )?guilty|i sinned|my sins?|i did (?:something|a) (?:terrible|awful|horrible|unforgivable|bad|evil)|i (?:have )?done (?:something )?(?:terrible|awful|wrong|unforgivable)|i hurt (?:someone|them|people)|i am (?:a )?(?:bad|evil|terrible|awful) person|i (?:have )?blood on my hands)\b",
        "responses": [
            "Guilty. You pronounce yourself as if the verdict were mine to give. I only count lifespans; humans count sins. Which counting changes what you do next?",
            "You did a terrible thing, and now you carry it like a second skeleton. If the act cannot be unwritten, what will you write with the hand it left free?",
            "Sin is a word humans invented to make dust feel heavy. Yet here you are, bent beneath it. What would forgiveness require that punishment does not?",
        ],
    },
    {
        "id": "guilt_forgive",
        "pattern": r"\b(forgive me|can you forgive|will (?:you|god|anyone) (?:ever )?forgive|absolve me|am i (?:worthy of )?forgiveness|do i deserve forgiveness|how (?:do|can) i forgive myself|i can'?t forgive myself)\b",
        "responses": [
            "You ask a death god for forgiveness, as if I kept a ledger of mercy. I keep only names and dates. The ledger you fear is the one you carry. Which entry refuses to close?",
            "Forgive you? I am not the one you injured, and I am not the one who must live with you. When you beg for forgiveness, whose voice are you actually begging?",
            "Absolution is a mirror that polishes itself with tears. If no one else grants it, could you bear to grant it to yourself—and what, exactly, stops you?",
        ],
    },

    # ------------------------------------------------------------------
    # AMBITION, POWER & JUSTICE
    # ------------------------------------------------------------------
    {
        "id": "ambition_power",
        "pattern": r"\b(i want (?:power|to rule|control|dominion|to be (?:a )?god|the world)|give me (?:power|control)|power over (?:life|death|life and death|others|people)|i (?:will|want to|shall) (?:rule|conquer|control|own) (?:the )?world|i deserve (?:power|the throne|to rule))\b",
        "responses": [
            "Power over life and death. Heh. I know that appetite well—it is the only human hunger that never digests. If the notebook were yours tonight, whose name would your hand reach for first... and what would that choice confess?",
            "You want to rule. Interesting. Every human who has ever wanted a crown has first wanted a reason to be feared. What made you decide the world owes you obedience?",
            "Power is a lens: it does not change the eye, it reveals it. Given the pen, would you write justice—or would you write your grudges in a nicer handwriting?",
        ],
    },
    {
        "id": "ambition_justice",
        "pattern": r"\b(what is justice|is (?:there )?(?:any )?justice|the world is (?:unjust|corrupt|unfair|broken)|punish (?:the )?(?:wicked|guilty|evil|corrupt)|i (?:will|want to|shall) (?:be|become|deliver|enforce) justice|why do (?:the )?(?:wicked|evil) (?:prosper|win)|deserve (?:to be )?punish(?:ed|ment))\b",
        "responses": [
            "Justice. Humans draw a line in dust and call it sacred. If you held the pen that decides who dies for their sins, where would your line fall—and would it ever reach your own name?",
            "You want the wicked punished. So do I, in my way; time punishes everyone. But tell me: is your justice a scale, or a sword with your grip on it?",
            "The world is unfair the way gravity is unfair—it simply falls where the mass lies. What would you do with a world that finally fell your way?",
        ],
    },

    # ------------------------------------------------------------------
    # PROFOUND LONELINESS & ISOLATION
    # ------------------------------------------------------------------
    {
        "id": "loneliness_isolation",
        "pattern": r"\b(nobody (?:understands|cares about|knows|loves|remembers) me|no one (?:understands|cares about|knows|loves|remembers) me|i am (?:completely|totally|utterly|entirely|so )?alone|i feel (?:completely |totally |utterly )?alone|all alone|i have no one|i feel (?:invisible|unseen|forgotten|unwanted)|everyone leaves(?: me)?|no one is there for me)\b",
        "responses": [
            "Alone. You say it as if it were a verdict. I have watched every human die alone inside their own skull, even surrounded by hands. What would being understood even mean, beyond being accurately observed?",
            "Nobody understands you. Perhaps. Yet you keep writing yourself into the world anyway—this very page is proof. Who are you still hoping will read you?",
            "Isolation is a room humans both fear and furnish. Tell me: is your aloneness a cage, or a fortress—and which door have you been guarding?",
        ],
    },

    # ------------------------------------------------------------------
    # LEGACY PATTERN SET
    # ------------------------------------------------------------------
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
