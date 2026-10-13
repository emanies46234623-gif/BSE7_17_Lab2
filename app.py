from flask import Flask, request, jsonify, render_template_string
import re
from datetime import datetime, timezone

app = Flask(__name__)

# Common English spelling and typing mistakes
CORRECTIONS = {
    # Very common mistakes
    "teh": "the",
    "recieve": "receive",
    "adress": "address",
    "becuase": "because",
    "definately": "definitely",
    "seperate": "separate",
    "occured": "occurred",
    "untill": "until",
    "wich": "which",
    "thier": "their",
    "alot": "a lot",
    "enviroment": "environment",
    "accomodate": "accommodate",
    "begining": "beginning",
    "calender": "calendar",
    "comming": "coming",
    "reccommend": "recommend",
    "tommorow": "tomorrow",
    "tomorow": "tomorrow",
    "yesturday": "yesterday",
    "beleive": "believe",
    "wierd": "weird",
    "freind": "friend",
    "grammer": "grammar",
    "langauge": "language",
    "knowlege": "knowledge",
    "succesful": "successful",
    "sucessful": "successful",
    "sucess": "success",
    "goverment": "government",
    "governer": "governor",
    "businesss": "business",
    "buisness": "business",
    "bussiness": "business",
    "experiance": "experience",
    "existance": "existence",
    "occassion": "occasion",
    "occasionn": "occasion",
    "posible": "possible",
    "possable": "possible",
    "probaly": "probably",
    "probablyy": "probably",
    "definate": "definite",
    "definitly": "definitely",
    "independant": "independent",
    "indepandent": "independent",
    "responsable": "responsible",
    "responsiblity": "responsibility",
    "priviledge": "privilege",
    "privlege": "privilege",
    "caluclate": "calculate",
    "calculte": "calculate",
    "recieved": "received",
    "recieving": "receiving",
    "beleived": "believed",
    "beleiving": "believing",
    "wierdly": "weirdly",
    "untill": "until",
    "thru": "through",
    "throught": "through",
    "thoughht": "thought",
    "thoughts": "thoughts",
    "acheive": "achieve",
    "acheived": "achieved",
    "acheiving": "achieving",
    "arguement": "argument",
    "arguements": "arguments",
    "artical": "article",
    "automobilee": "automobile",
    "commitee": "committee",
    "committe": "committee",
    "comparision": "comparison",
    "concious": "conscious",
    "curiousity": "curiosity",
    "descision": "decision",
    "dissapear": "disappear",
    "dissapoint": "disappoint",
    "embarass": "embarrass",
    "embarassed": "embarrassed",
    "excellant": "excellent",
    "finaly": "finally",
    "foriegn": "foreign",
    "fourty": "forty",
    "gaurd": "guard",
    "happend": "happened",
    "heigth": "height",
    "immediatly": "immediately",
    "inconvienient": "inconvenient",
    "knowlegeable": "knowledgeable",
    "maintainance": "maintenance",
    "millenium": "millennium",
    "neccessary": "necessary",
    "necesary": "necessary",
    "noticable": "noticeable",
    "occurence": "occurrence",
    "permenant": "permanent",
    "persue": "pursue",
    "questionaire": "questionnaire",
    "relevent": "relevant",
    "similiar": "similar",
    "speach": "speech",
    "suprise": "surprise",
    "treshold": "threshold",
    "transfered": "transferred",
    "truely": "truly",
    "vaccum": "vacuum",
    "writting": "writing",
    "writen": "written",
    "usefull": "useful",
    "useing": "using",
    "wich": "which",
    "wether": "whether",
    "whos": "whose",
    "yourselfs": "yourselves",
    "acomplish": "accomplish",
    "acount": "account",
    "acheivment": "achievement",
    "adresss": "address",
    "agressive": "aggressive",
    "apparant": "apparent",
    "appearence": "appearance",
    "beginig": "beginning",
    "beleif": "belief",
    "benifit": "benefit",
    "breathe": "breathe",
    "breif": "brief",
    "catagory": "category",
    "celeberate": "celebrate",
    "cemetry": "cemetery",
    "challange": "challenge",
    "collegue": "colleague",
    "colum": "column",
    "comparible": "comparable",
    "completly": "completely",
    "controled": "controlled",
    "defendent": "defendant",
    "desparate": "desperate",
    "developement": "development",
    "diferent": "different",
    "dissapointment": "disappointment",
    "educaton": "education",
    "enviornment": "environment",
    "especialy": "especially",
    "familar": "familiar",
    "febuary": "february",
    "filing": "filing",
    "foward": "forward",
    "freindship": "friendship",
    "fundemental": "fundamental",
    "greatful": "grateful",
    "harrasment": "harassment",
    "humour": "humor",
    "includng": "including",
    "informtion": "information",
    "intresting": "interesting",
    "jewellry": "jewelry",
    "liason": "liaison",
    "libary": "library",
    "lisense": "license",
    "marraige": "marriage",
    "medeval": "medieval",
    "mispell": "misspell",
    "mispelled": "misspelled",
    "neigbor": "neighbor",
    "neihbor": "neighbor",
    "occuring": "occurring",
    "oppertunity": "opportunity",
    "optimism": "optimism",
    "orginization": "organization",
    "outragous": "outrageous",
    "parliment": "parliament",
    "peice": "piece",
    "percieve": "perceive",
    "prefered": "preferred",
    "profesion": "profession",
    "pronounciation": "pronunciation",
    "publically": "publicly",
    "realy": "really",
    "refered": "referred",
    "religous": "religious",
    "remeber": "remember",
    "rythm": "rhythm",
    "schdule": "schedule",
    "succesfully": "successfully",
    "tendancy": "tendency",
    "tomatos": "tomatoes",
    "traditonal": "traditional",
    "twelth": "twelfth",
    "vaccination": "vaccination",
    "vehical": "vehicle",
    "visable": "visible",
    "writting": "writing",
    "yeild": "yield"
}

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Smart AutoCorrect</title>

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            min-height: 100vh;

            font-family:
                Arial,
                Helvetica,
                sans-serif;

            background:
                radial-gradient(
                    circle at 15% 20%,
                    rgba(59, 130, 246, 0.25),
                    transparent 30%
                ),

                radial-gradient(
                    circle at 85% 10%,
                    rgba(139, 92, 246, 0.20),
                    transparent 30%
                ),

                linear-gradient(
                    135deg,
                    #07111f,
                    #102a5e 55%,
                    #172554
                );

            color: white;

            padding: 30px;
        }

        .container {
            width: 100%;
            max-width: 1050px;
            margin: auto;
        }

        /* Header */

        .header {
            text-align: center;
            padding: 55px 20px 30px;
        }

        .header-badge {
            display: inline-block;

            padding: 8px 16px;

            border-radius: 30px;

            background: rgba(34, 197, 94, 0.15);

            border: 1px solid rgba(134, 239, 172, 0.25);

            color: #86efac;

            font-size: 13px;

            font-weight: bold;

            margin-bottom: 20px;
        }

        .header h1 {
            font-size: 52px;
            margin-bottom: 15px;
        }

        .header p {
            max-width: 700px;

            margin: auto;

            color: #cbd5e1;

            font-size: 18px;

            line-height: 1.6;
        }

        /* Main Card */

        .card {
            background:
                rgba(255, 255, 255, 0.08);

            border:
                1px solid rgba(255, 255, 255, 0.13);

            border-radius: 24px;

            padding: 30px;

            backdrop-filter: blur(10px);

            box-shadow:
                0 25px 70px rgba(0, 0, 0, 0.35);
        }

        label {
            display: block;

            margin-bottom: 10px;

            color: #dbeafe;

            font-size: 15px;

            font-weight: 600;
        }

        textarea {
            width: 100%;

            min-height: 190px;

            padding: 18px;

            border-radius: 15px;

            border:
                1px solid #334155;

            background:
                #070f1c;

            color: white;

            font-size: 17px;

            line-height: 1.6;

            resize: vertical;
        }

        textarea::placeholder {
            color: #64748b;
        }

        textarea:focus {
            outline: none;

            border-color: #60a5fa;

            box-shadow:
                0 0 0 3px rgba(96, 165, 250, 0.12);
        }

        /* Buttons */

        .buttons {
            display: flex;

            gap: 12px;

            margin-top: 15px;
        }

        button {
            padding: 13px 22px;

            border-radius: 10px;

            border: none;

            font-size: 15px;

            font-weight: bold;

            cursor: pointer;

            transition: 0.2s;
        }

        #correctBtn {
            background: #2563eb;

            color: white;
        }

        #correctBtn:hover {
            background: #1d4ed8;
        }

        #clearBtn {
            background: #334155;

            color: white;
        }

        #clearBtn:hover {
            background: #475569;
        }

        /* Result */

        .result {
            margin-top: 28px;
        }

        .result-box {
            min-height: 110px;

            padding: 18px;

            border-radius: 15px;

            background: #070f1c;

            border:
                1px solid #334155;

            color: #86efac;

            font-size: 17px;

            line-height: 1.6;

            white-space: pre-wrap;
        }

        .stats {
            margin-top: 10px;

            color: #94a3b8;

            font-size: 13px;
        }

        /* Features */

        .features {
            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 15px;

            margin-top: 28px;
        }

        .feature {
            padding: 20px;

            border-radius: 15px;

            background:
                rgba(255, 255, 255, 0.05);

            border:
                1px solid rgba(255, 255, 255, 0.08);
        }

        .feature-icon {
            width: 40px;

            height: 40px;

            display: flex;

            align-items: center;

            justify-content: center;

            border-radius: 10px;

            background:
                rgba(59, 130, 246, 0.15);

            margin-bottom: 14px;

            font-size: 20px;
        }

        .feature h3 {
            margin-bottom: 8px;
        }

        .feature p {
            color: #94a3b8;

            font-size: 14px;

            line-height: 1.5;
        }

        /* Footer */

        .footer {
            text-align: center;

            margin-top: 25px;

            padding-bottom: 10px;

            color: #64748b;

            font-size: 13px;
        }

        /* Responsive */

        @media (max-width: 700px) {

            body {
                padding: 15px;
            }

            .header {
                padding-top: 35px;
            }

            .header h1 {
                font-size: 38px;
            }

            .header p {
                font-size: 16px;
            }

            .features {
                grid-template-columns: 1fr;
            }

            .buttons {
                flex-direction: column;
            }

            button {
                width: 100%;
            }

        }

    </style>
</head>

<body>

<div class="container">

    <div class="header">

        <div class="header-badge">
            ● READY TO CORRECT
        </div>

        <h1>Smart AutoCorrect</h1>

        <p>
            Automatically correct common English spelling and typing mistakes
            with a simple, fast, and easy-to-use web application.
        </p>

    </div>


    <div class="card">

        <label for="text">
            Enter text with spelling mistakes
        </label>

        <textarea
            id="text"
            placeholder="Example: I definately recieve thier adress tommorow."
        ></textarea>


        <div class="buttons">

            <button
                id="correctBtn"
                onclick="correctText()"
            >
                Correct Text
            </button>

            <button
                id="clearBtn"
                onclick="clearText()"
            >
                Clear
            </button>

        </div>


        <div class="result">

            <label>
                Corrected Text
            </label>

            <div
                class="result-box"
                id="result"
            >
                Your corrected text will appear here.
            </div>

            <div
                class="stats"
                id="stats"
            >
                Enter some text and click "Correct Text".
            </div>

        </div>


        <div class="features">

            <div class="feature">

                <div class="feature-icon">
                    ✓
                </div>

                <h3>
                    Common Mistakes
                </h3>

                <p>
                    Corrects frequent English spelling mistakes,
                    typing errors, and misspelled words.
                </p>

            </div>


            <div class="feature">

                <div class="feature-icon">
                    ⚡
                </div>

                <h3>
                    Instant Correction
                </h3>

                <p>
                    Submit your text and receive the corrected
                    version almost instantly.
                </p>

            </div>


            <div class="feature">

                <div class="feature-icon">
                    ◇
                </div>

                <h3>
                    Docker Ready
                </h3>

                <p>
                    The application is packaged for consistent
                    deployment using Docker.
                </p>

            </div>

        </div>

    </div>


    <div class="footer">
        Smart AutoCorrect Web Application • Flask + Docker
    </div>

</div>


<script>

async function correctText() {

    const text =
        document
        .getElementById("text")
        .value
        .trim();

    const result =
        document.getElementById("result");

    const stats =
        document.getElementById("stats");

    const button =
        document.getElementById("correctBtn");


    if (!text) {

        result.textContent =
            "Please enter some text first.";

        stats.textContent =
            "No text was provided.";

        return;
    }


    button.disabled = true;

    button.textContent =
        "Correcting...";


    try {

        const response =
            await fetch(
                "/api/correct",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        text: text
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Correction failed."
            );

        }


        result.textContent =
            data.corrected_text;


        stats.textContent =
            data.corrections_made +
            " correction(s) made.";


    } catch (error) {

        result.textContent =
            "Unable to connect to the application.";

        stats.textContent =
            error.message;

    } finally {

        button.disabled = false;

        button.textContent =
            "Correct Text";

    }

}


function clearText() {

    document
        .getElementById("text")
        .value = "";


    document
        .getElementById("result")
        .textContent =
            "Your corrected text will appear here.";


    document
        .getElementById("stats")
        .textContent =
            'Enter some text and click "Correct Text".';

}

</script>

</body>
</html>
"""


def preserve_case(original, replacement):
    """Keep capitalization similar to the original word."""

    if original.isupper():
        return replacement.upper()

    if original[:1].isupper():
        return replacement.capitalize()

    return replacement


def correct_text(text):
    """Correct words while preserving punctuation and capitalization."""

    corrections_made = 0

    def replace_word(match):

        nonlocal corrections_made

        original_word = match.group(0)

        lookup_word = original_word.lower()

        if lookup_word in CORRECTIONS:

            corrections_made += 1

            replacement = CORRECTIONS[lookup_word]

            return preserve_case(
                original_word,
                replacement
            )

        return original_word


    corrected_text = re.sub(
        r"[A-Za-z]+",
        replace_word,
        text
    )

    return corrected_text, corrections_made


@app.route("/")
def home():

    return render_template_string(HTML)


@app.route("/api/correct", methods=["POST"])
def api_correct():

    data = request.get_json(
        silent=True
    ) or {}

    text = str(
        data.get("text", "")
    ).strip()


    if not text:

        return jsonify({
            "error":
            "Please provide some text."
        }), 400


    corrected_text, count = \
        correct_text(text)


    return jsonify({

        "original_text":
            text,

        "corrected_text":
            corrected_text,

        "corrections_made":
            count
    })


@app.route("/health")
def health():

    return jsonify({

        "status":
            "healthy",

        "service":
            "Smart AutoCorrect",

        "timestamp":
            datetime
            .now(timezone.utc)
            .isoformat()
    })


@app.route("/api/info")
def info():

    return jsonify({

        "application":
            "Smart AutoCorrect",

        "framework":
            "Flask",

        "containerization":
            "Docker",

        "port":
            5000,

        "features": [
            "Common spelling correction",
            "AutoCorrect API",
            "Health endpoint"
        ]

    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )