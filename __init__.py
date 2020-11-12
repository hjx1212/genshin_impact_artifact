from random import randrange, choice, choices, random

from hoshino import Service
sv = Service('原神圣遗物')


AUTO_ENHANCE = True

suit = [
    # 0
    ("平息鸣雷的尊者", ("平雷之心", "平雷之羽", "平雷之刻", "平雷之器", "平雷之冠"),
     ("雷元素抗性提高40%。", "对处于雷元素影响下的敌人造成的伤害提升35%。"),
     ("平雷套", "平雷")),
    # 1
    ("渡过烈火的贤人", ("渡火者的决绝", "渡火者的解脱", "渡火者的煎熬", "渡火者的醒悟", "渡火者的智慧"),
     ("火元素抗性提高40%。", "对处于火元素影响下的敌人造成的伤害提升35%。"),
     ("渡火者套", "渡火套", "渡火者", "渡火")),
    # 2
    ("被怜爱的少女", ("远方的少女之心", "少女飘摇的思念", "少女苦短的良辰", "少女片刻的闲暇", "少女易逝的芳颜"),
     ("角色造成的治疗效果提升15%。", "施放元素战技或元素爆发后的10秒内，队伍中所有角色受治疗效果加成提高20%。"),
     ("少女套", "治疗套", "少女")),
    # 3
    ("角斗士的终幕礼", ("角斗士的留恋", "角斗士的归宿", "角斗士的希冀", "角斗士的酣醉", "角斗士的凯旋"),
     ("攻击力提高18%。", "装备该圣遗物套装的角色为单手剑、双手剑、长柄武器角色时，角色普通攻击造成的伤害提高35%。"),
     ("角斗士套", "角斗士")),
    # 4
    ("翠绿之影", ("野花记忆的绿野", "猎人青翠的箭羽", "翠绿猎人的笃定", "翠绿猎人的容器", "翠绿的猎人之冠"),
     ("获得15%风元素伤害加成。", "扩散反应造成的伤害提升60%。根据扩散的元素类型，降低受到影响的敌人40%的对应元素抗性，持续10秒。"),
     ("翠绿套", "风套", "翠绿")),
    # 5
    ("流浪大地的乐团", ("乐团的晨光", "琴师的箭羽", "终幕的时计", "吟游者之壶", "指挥的礼帽"),
     ("元素精通提高80点。", "装备该圣遗物套装的角色为法器、弓箭角色时，角色重击造成的伤害提高35%。"),
     ("流浪大地套", "流浪大地")),
    # 6
    ("如雷的盛怒", ("雷鸟的怜悯", "雷灾的孑遗", "雷霆的时计", "降雷的凶兆", "唤雷的头冠"),
     ("获得15%雷元素伤害加成。", "超载、感电、超导反应造成的伤害提升40%。触发这些元素反应时，元素战技冷却时间减少1秒。该效果每0.8秒最多触发一次。"),
     ("如雷套", "雷套", "如雷")),
    # 7
    ("炽烈的炎之魔女", ("魔女的炎之花", "魔女常燃之羽", "魔女破灭之时", "魔女的心之火", "焦灼的魔女帽"),
     ("获得15%火元素伤害加成。", "超载、燃烧反应造成的伤害提升40%，蒸发、融化反应的加成系数提高15%。施放元素战技后的10秒内，2件套的效果提高50%，该效果最多叠加3次。"),
     ("魔女套", "火套", "魔女")),
    # 8
    ("昔日宗室之仪", ("宗室之花", "宗室之翎", "宗室时计", "宗室银瓮", "宗室面具"),
     ("元素爆发造成的伤害提升20％。", "施放元素爆发后，队伍中所有角色攻击力提升20％，持续12秒。该效果不可叠加。"),
     ("宗室套", "宗室")),
    # 9
    ("染血的骑士道", ("染血的铁之心", "染血的黑之羽", "骑士染血之时", "染血骑士之杯", "染血的铁假面"),
     ("造成的物理伤害提高25%。", "击败敌人后的10秒内，施放重击时不消耗体力，且造成的伤害提升50%。"),
     ("染血套", "骑士套", "物理套", "染血", "骑士")),
    # 10
    ("悠古的磐岩", ("磐陀裂生之花", "嵯峨群峰之翼", "星罗圭壁之晷", "巉岩琢塑之樽", "不动玄石之相"),
     ("获得15%岩元素伤害加成。", "获得岩元素反应形成的晶片时，队伍中所有角色获得35%对应元素伤害加成，持续10秒。同时只能通过该效果获得一种元素伤害加成。"),
     ("磐岩套", "岩套", "磐岩")),
    # 11
    ("逆飞的流星", ("夏祭之花", "夏祭终末", "夏祭之刻", "夏祭水玉", "夏祭之面"),
     ("护盾强效提高35%。", "处于护盾庇护下时，额外获得40%普通攻击和重击伤害加成。"),
     ("流星套", "夏祭套", "流星", "夏祭")),
    # 12
    ("征服寒冬的勇士", ("碎冰者的思念", "碎冰者的自矜", "碎冰者的终期", "碎冰者的傲骨", "碎冰者的骄傲"),
     ("冰元素抗性提高40%。", "对处于冻结状态及冰元素影响下的敌人造成的伤害提升35%。"),
     ("寒冬套", "碎冰者套", "碎冰套", "寒冬", "碎冰者", "碎冰")),
    # 13
    ("冰之川与雪之砂", ("凛冬霜心", "雪藏之羽", "凝冰成砂", "北风之盏", "冰河之冠"),
     ("获得15%冰元素伤害加成。", "超导反应造成的伤害提升50%，融化反应加成系数提高15%，施放元素爆发后的10秒内，冰元素伤害加成额外提升25%。"),
     ("冰雪套", "冰套", "冰雪")),
]
slot = [
    ("生之花", ("花",)),
    ("死之羽", ("羽", "羽毛")),
    ("时之沙", ("沙", "沙漏")),
    ("空之杯", ("杯", "杯子")),
    ("理之冠", ("冠", "头", "帽子", "帽")),
]

attrs = [
    # 0
    ("生命值", 717, 4780, (209, 239, 269, 299),
     ()),
    # 1
    ("生命值", .070, .466, (.041, .047, .053, .058),
     ("生命", "生", "血")),
    # 2
    ("攻击力", 47, 311, (14, 16, 18, 19),
     ()),
    # 3
    ("攻击力", .070, .466, (.041, .047, .053, .058),
     ("攻击", "攻")),
    # 4
    ("防御力", None, None, (16, 19, 21, 23),
     ()),
    # 5
    ("防御力", .087, .583, (.051, .058, .066, .073),
     ("防御", "防")),
    # 6
    ("元素精通", 28, 187, (16, 19, 21, 23),
     ("元素", "精通")),
    # 7
    ("元素充能效率", .078, .518, (.045, .052, .058, .065),
     ("元素充能", "充能效率", "充能")),
    # 8
    ("暴击率", .047, .311, (.027, .031, .035, .039),
     ("暴击", "暴率", "暴")),
    # 9
    ("暴击伤害", .093, .622, (.054, .062, .070, .078),
     ("暴伤", )),
    # 10
    ("物理伤害加成", .087, .583, None,
     ("物理", "物", "物伤")),
    # 11
    ("火元素伤害加成", .070, .466, None,
     ("火元素", "火", "火伤")),
    # 12
    ("水元素伤害加成", .070, .466, None,
     ("水元素", "水", "水伤")),
    # 13
    ("雷元素伤害加成", .070, .466, None,
     ("雷元素", "雷", "雷伤")),
    # 14
    ("冰元素伤害加成", .070, .466, None,
     ("冰元素", "冰", "冰伤")),
    # 15
    ("风元素伤害加成", .070, .466, None,
     ("风元素", "风", "风伤")),
    # 16
    ("岩元素伤害加成", .070, .466, None,
     ("岩元素", "岩", "岩伤")),
    # 17
    ("治疗加成", .054, .359, None,
     ("治疗",)),
]

available_main_attrs = [(0,), (2,), (1, 3, 5, 6, 7), (1, 3, 5, 6, 10, 11, 12, 13, 14, 15, 16), (1, 3, 5, 6, 8, 9, 17)]
available_sub_attrs = [(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)] * 5

max_attr = 4
attr_rate = (1., 1., 1., .25, .0)
sub_attr_value_weight = (10, 35, 35, 20)

dungeon = [
    ("精英级怪物,BOSS级怪物", (3, 5),    # 角斗士的终幕礼, 流浪大地的乐团
     ("精英", "BOSS", "无相", "龙", "狼")),
    ("无妄引咎密宫：祝圣秘境：寒霜", (1, 7),  # 渡过烈火的贤人, 炽烈的炎之魔女
     ("无妄引咎密宫", "寒霜", "火本")),
    ("仲夏庭园：祝圣秘境：净化之炎", (0, 6),  # 平息鸣雷的尊者, 如雷的盛怒
     ("仲夏庭园", "净化之炎", "雷本")),
    ("孤云凌霄之处：祝圣秘境：惊蛰", (10, 11),  # 悠古的磐岩, 逆飞的流星
     ("孤云凌霄之处", "惊蛰", "岩本")),
    ("铭记之谷：祝圣秘境：钢铁之舞", (2, 4),  # 被怜爱的少女, 翠绿之影
     ("铭记之谷", "钢铁之舞", "风本", "少女本", "治疗本")),
    ("华池岩岫：祝圣秘境：岩牢", (9, 8),    # 染血的骑士道, 昔日宗室之仪
     ("华池岩岫", "岩牢", "物理本")),
    ("???????????????", (12, 13),    # 征服寒冬的勇士, 冰之川与雪之砂
     ("冰本",))
]

keyword_max_len = 10
keywords = {}
for i, v in enumerate(suit):
    keywords[v[0]] = {"suit": i}
    for ii, vv in enumerate(v[1]):
        keywords[vv] = {"suit": i, "slot": ii}
    for vv in v[-1]:
        keywords[vv] = {"suit": i}
for i, v in enumerate(slot):
    keywords[v[0]] = {"slot": i}
    for vv in v[-1]:
        keywords[vv] = {"slot": i}
for i, v in enumerate(attrs):
    keywords[v[0]] = {"main_attr": i}
    for vv in v[-1]:
        keywords[vv] = {"main_attr": i}
for i, v in enumerate(dungeon):
    for vv in v[-1]:
        keywords[vv] = {"dungeon": i}


def enhance_sub_attr(artifact):
    if len(artifact["sub_attr"]) < max_attr:
        while True:
            attr_id = choice(available_sub_attrs[artifact["slot"]])
            if artifact["main_attr"]["id"] == attr_id:
                continue
            for sub_attr in artifact["sub_attr"]:
                if sub_attr["id"] == attr_id:
                    attr_id = -1
                    break
            if attr_id < 0:
                continue
            attr_value = choices(attrs[attr_id][3], sub_attr_value_weight)[0]
            artifact["sub_attr"].append({"id": attr_id, "value": attr_value})
            break
    else:
        sub_attr = choice(artifact["sub_attr"])
        attr_id = sub_attr["id"]
        attr_value = choices(attrs[attr_id][3], sub_attr_value_weight)[0]
        sub_attr["value"] += attr_value
    return attr_id, attr_value


def enhance(artifact):
    ret = '强化:'
    while artifact["level"] < 20:
        artifact["level"] = (artifact["level"] // 4 + 1) * 4
        artifact["main_attr"]["value"] = attrs[artifact["main_attr"]["id"]][2]
        attr_id, attr_value = enhance_sub_attr(artifact)
        ret += f' {attrs[attr_id][0]}'
    return ret


def get_rand_artifact(suit_id=None):
    suit_id = suit_id if isinstance(suit_id, int) else choice(suit_id) if suit_id else randrange(len(suit))
    slot_id = randrange(len(slot))
    main_attr_id = choice(available_main_attrs[slot_id])
    artifact = {
        "suit": suit_id,
        "slot": slot_id,
        "level": 0,
        "main_attr": {"id": main_attr_id, "value": attrs[main_attr_id][1]},
        "sub_attr": [],
    }
    attr_p = random()
    while attr_p < attr_rate[len(artifact["sub_attr"])]:
        enhance_sub_attr(artifact)
    return artifact


def print_artifact(artifact):
    ret = ''
    ret += f'{suit[artifact["suit"]][1][artifact["slot"]]} +{artifact["level"]}\n'
    ret += f'{slot[artifact["slot"]][0]}\n'
    attr = artifact["main_attr"]
    ret += f'{attrs[attr["id"]][0]}+{attr["value"]:{"d" if isinstance(attr["value"], int) else ".1%"}}\n'
    ret += f'★★★★★\n'
    for attr in artifact["sub_attr"]:
        ret += f'· {attrs[attr["id"]][0]}+{attr["value"]:{"d" if isinstance(attr["value"], int) else ".1%"}}\n'
    ret += f'{suit[artifact["suit"]][0]}'
    return ret


def parse_content(content):
    content = content.strip()
    target = {"dungeon": None, "suit": None, "slot": None, "main_attr": None}
    while content:
        ok = False
        for i in range(min(len(i), keyword_max_len), 0, -1):
            ret = keywords.get(content[:i])
            if ret:
                for k, v in ret.items():
                    if target.get(k):
                        raise ValueError(f'重复关键词: {content[:i]}')
                    target[k] = v
                content = content[i:].strip()
                ok = True
                break
        if not ok:
            raise ValueError(f'没有找到关键词: {content}')

    if target["suit"]:
        dungeon_id = None
        for i, v in enumerate(dungeon):
            if target["suit"] in v[1]:
                dungeon_id = i
                break
        if not target["dungeon"]:
            target["dungeon"] = dungeon_id
        elif target["dungeon"] != dungeon_id:
            raise ValueError(f'圣遗物套装与所刷取的秘境不符')
    if target["slot"] and target["main_attr"]:
        if target["slot"] in (0, 1):
            target["main_attr"] -= 1    # trick...
        if target["main_attr"] not in available_main_attrs[target["slot"]]:
            raise ValueError(f'圣遗物位置的主属性不符')

    return target


@sv.on_prefix(["圣遗物", "原神圣遗物"], only_to_me=True)
async def genshin_artifact(bot, ev):
    try:
        target = parse_content(ev.message.extract_plain_text())
    except Exception as e:
        await bot.send(ev, e)
        return
    target_dungeon = dungeon[target["dungeon"]] if target["dungeon"] else None
    times = 0
    while True:
        artifact = get_rand_artifact(target_dungeon[1] if target_dungeon else None)
        times += 1
        if target["suit"] and target["suit"] != artifact["suit"]:
            continue
        if target["slot"] and target["slot"] != artifact["slot"]:
            continue
        if target["main_attr"] and target["main_attr"] != artifact["main_attr"]["id"]:
            continue
        break
    msg = f'刷取{target_dungeon[0] if target_dungeon else ""}圣遗物{times}次，获得:\n{print_artifact(artifact)}'
    if AUTO_ENHANCE:
        msg += f'\n\n{enhance(artifact)}\n'
        msg += print_artifact(artifact)
    await bot.send(ev, msg, at_sender=True)


if __name__ == '__main__':
    # main()

    test = {
        "suit": 0, "slot": 0, "level": 0, "main_attr": {"id": 0, "value": 717},
        "sub_attr": [{"id": 6, "value": 19}, {"id": 8, "value": .035}, {"id": 9, "value": .078}],
    }
    print(print_artifact(test))
    enhance(test)
    print(print_artifact(test))

    print(print_artifact(get_rand_artifact()))