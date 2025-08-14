from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# 🔹 MongoDB 연결 (URI는 본인 환경에 맞게 수정하세요)
uri = "mongodb+srv://<아이디>:<비밀번호>@cluster0.ggmnw83.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, 27017)
db = client.dbjungle  # DB 이름

# ✅ 메인 페이지
@app.route('/')
def home():
    return render_template('index.html')

# ✅ 리뷰 저장 API
@app.route('/review', methods=['POST'])
def post_review():
    data = request.get_json()
    theme = data.get('theme')
    nickname = data.get('nickname')
    rating = data.get('rating')
    review_text = data.get('review')

    if not theme or not nickname or not rating or not review_text:
        return jsonify({'result': 'fail', 'msg': '모든 필드를 입력하세요.'})

    review_doc = {
        'theme': theme,
        'nickname': nickname,
        'rating': int(rating),
        'review': review_text
    }
    db.reviews.insert_one(review_doc)

    return jsonify({'result': 'success'})

# ✅ 리뷰 조회 API
@app.route('/review', methods=['GET'])
def get_reviews():
    theme = request.args.get('theme')
    if not theme:
        return jsonify({'result': 'fail', 'msg': '테마를 지정하세요.'})

    reviews = list(db.reviews.find({'theme': theme}, {'_id': 0}))
    return jsonify({'result': 'success', 'reviews': reviews})

# ✅ 서버 실행
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)