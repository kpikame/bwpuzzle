from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)


@app.route('/api/submit_bug', methods=['POST'])
def submit_bug():
    data = request.json
    bug_report = data.get('bug_report', '')

    # 这里可以添加将bug_report保存到数据库或发送邮件的逻辑
    # 例如：save_to_database(bug_report)

    print(f"Received bug report: {bug_report}")  # 临时打印到控制台
    return jsonify({'status': 'success', 'message': 'Bug报告已提交，感谢反馈！'})

# 加载百闻牌卡牌数据
def load_card_data():
    with open('card_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 随机获取一张百闻牌卡牌
@app.route('/api/puzzle', methods=['GET'])
def get_puzzle():
    cards = load_card_data()
    puzzle = random.choice(cards)
    return jsonify(puzzle)

# 获取所有百闻牌卡牌数据（包括shikigaminame）
@app.route('/api/card_names', methods=['GET'])
def get_card_names():
    cards = load_card_data()
    return jsonify(cards)  # 返回完整的卡牌对象数组

# 检查答案并返回反馈
@app.route('/api/check', methods=['POST'])
def check_answer():
    data = request.json
    user_answer = data.get('answer', '').lower()
    target_card = data.get('targetCard', {})

    # 初始化反馈
    feedback = {
        'name': 'default',
        'shikigaminames': 'default',
        'shikigamipositions': 'default',
        'factions': 'default',
        'cardtype': 'default',
        'atkchange': 'default',
        'hpchange': 'default',
        'terms': 'default',
        'level': 'default',
        'rarity': 'default',
        'cardpack': 'default'
    }

    # 假设我们有一个目标百闻牌卡牌
    target_name = target_card['name'].lower()
    target_shikigaminames = target_card['shikigaminames']
    target_shikigamipositions = target_card['shikigamipositions']
    target_factions = target_card['factions']
    target_cardtype = target_card['cardtype']
    target_atkchange = target_card['atkchange']
    target_hpchange = target_card['hpchange']
    target_terms = target_card['terms']
    target_level = target_card['level']
    target_rarity = target_card['rarity']
    target_cardpack = target_card['cardpack']

    # 查找用户输入的百闻牌卡牌
    user_card = None
    for p in load_card_data():
        if p['name'].lower() == user_answer:
            user_card = p
            break

    if user_card:
        # 检查名称是否正确
        if user_answer == target_name:
            feedback['name'] = 'correct'
        else:
            feedback['name'] = 'incorrect'

        # 检查数值类型属性
        if user_card['atkchange'] == target_atkchange:
            feedback['atkchange'] = 'correct'
        elif user_card['atkchange'] - target_atkchange > 3:
            feedback['atkchange'] = 'higher'
        elif user_card['atkchange'] - target_atkchange < -3:
            feedback['atkchange'] = 'lower'
        elif (user_card['atkchange'] - target_atkchange >= -3) and (user_card['atkchange'] - target_atkchange < 0):
            feedback['atkchange'] = 'lower_and_near'
        else:
            feedback['atkchange'] = 'higher_and_near'

        if user_card['hpchange'] == target_hpchange:
            feedback['hpchange'] = 'correct'
        elif user_card['hpchange'] - target_hpchange > 3:
            feedback['hpchange'] = 'higher'
        elif user_card['hpchange'] - target_hpchange < -3:
            feedback['hpchange'] = 'lower'
        elif (user_card['hpchange'] - target_hpchange >= -3) and (user_card['hpchange'] - target_hpchange < 0):
            feedback['hpchange'] = 'lower_and_near'
        else:
            feedback['hpchange'] = 'higher_and_near'

        # 检查文字类型属性
        if set(user_card['shikigaminames']) == set(target_shikigaminames):
            feedback['shikigaminames'] = 'correct'
        elif any(t in target_shikigaminames for t in user_card['shikigaminames']):
            feedback['shikigaminames'] = 'partial'
        else:
            feedback['shikigaminames'] = 'incorrect'

        if set(user_card['shikigamipositions']) == set(target_shikigamipositions):
            feedback['shikigamipositions'] = 'correct'
        elif any(t in target_shikigamipositions for t in user_card['shikigamipositions']):
            feedback['shikigamipositions'] = 'partial'
        else:
            feedback['shikigamipositions'] = 'incorrect'

        if set(user_card['factions']) == set(target_factions):
            feedback['factions'] = 'correct'
        else:
            feedback['factions'] = 'incorrect'

        if set(user_card['cardtype']) == set(target_cardtype):
            feedback['cardtype'] = 'correct'
        else:
            feedback['cardtype'] = 'incorrect'

        if set(user_card['terms']) == set(target_terms):
            feedback['terms'] = 'correct'
        elif any(t in target_terms for t in user_card['terms']):
            feedback['terms'] = 'partial'
        else:
            feedback['terms'] = 'incorrect'

        raritys = ["无稀有度", "R", "SR", "SSR"]
        if user_card['rarity'] == target_rarity:
            feedback['rarity'] = 'correct'
        elif raritys.index(user_card['rarity']) < raritys.index(target_rarity):
            feedback['rarity'] = 'lower'
        elif raritys.index(user_card['rarity']) > raritys.index(target_rarity):
            feedback['rarity'] = 'higher'

        levels = ["无等级", 1, 2, 3]
        if user_card['level'] == target_level:
            feedback['level'] = 'correct'
        elif levels.index(user_card['level']) < levels.index(target_level):
            feedback['level'] = 'lower'
        elif levels.index(user_card['level']) > levels.index(target_level):
            feedback['level'] = 'higher'

        cardpacks = ["经典", "不夜之火", "月夜幻响", "沧海刀鸣", "吉运缘结", "四相琉璃", "善恶无明", "繁花入梦", "浮生方醒", "喧哗烩战",
                     "空弦绮话", "振剑归川", "远山遥泽", "鸣雷启蛰", "燃灯志异", "尘世轮回", "桃源故里", "祝星启明", "湮灭双生",
                     "千录晴诗", "龙渊秘境", "星缘百策"]
        if user_card['cardpack'] == target_cardpack:
            feedback['cardpack'] = 'correct'
        elif cardpacks.index(user_card['cardpack']) - cardpacks.index(target_cardpack) < -5:
            feedback['cardpack'] = 'lower'
        elif cardpacks.index(user_card['cardpack']) - cardpacks.index(target_cardpack) > 5:
            feedback['cardpack'] = 'higher'
        elif (cardpacks.index(user_card['cardpack']) - cardpacks.index(target_cardpack) >= -5) and (cardpacks.index(user_card['cardpack']) - cardpacks.index(target_cardpack) < 0):
            feedback['cardpack'] = 'lower_and_near'
        else:
            feedback['cardpack'] = 'higher_and_near'

    else:
        feedback['name'] = 'incorrect'

    return jsonify({'feedback': feedback, 'targetCard': target_card, 'userCard': user_card})

# 主页路由
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)