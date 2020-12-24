import os
import base64
from io import BytesIO
from random import randrange, choice, choices, random
from PIL import Image, ImageFont, ImageDraw, ImageMath

from .artifact_data import *

from hoshino import Service

sv = Service('原神圣遗物')

AUTO_ENHANCE = True
CONTENT_SUB_ATTR_PREFIX = "副"

for v in slot.values():
    v["main"] = [k for k, c in v["main_weight"].items() for _ in range(c)]
    v["sub"] = [k for k, c in v["sub_weight"].items() for _ in range(c)]

keyword_max_len = 10
keywords = {}
for k, v in suit.items():
    keywords[k] = {"suit": k}
    for kk in slot.keys():
        keywords[v[kk]] = {"suit": k, "slot": kk}
    for vv in v["alias"]:
        keywords[vv] = {"suit": k}
for k, v in slot.items():
    keywords[k] = {"slot": k}
    for vv in v["alias"]:
        keywords[vv] = {"slot": k}
for k, v in attrs.items():
    if keywords.get(k, {}).get("main_attr"):
        keywords[k]["main_attr"].add(k)
    else:
        keywords[k] = {"main_attr": {k}}
    for vv in v["alias"]:
        if keywords.get(vv, {}).get("main_attr"):
            keywords[vv]["main_attr"].add(k)
        else:
            keywords[vv] = {"main_attr": {k}}
for k, v in dungeon.items():
    for vv in v["alias"]:
        keywords[vv] = {"dungeon": k}

RES_PATH = os.path.join(os.path.dirname(__file__), 'res')
background = Image.open(os.path.join(RES_PATH, 'background.png')).resize((550, 570))
ttf_path = os.path.join(RES_PATH, "zh-cn.ttf")


def enhance_sub_attr(artifact):
    if len(artifact["sub_attr"]) < max_attr:
        while True:
            attr_name = choice(slot[artifact["slot"]]["sub"])
            if artifact["main_attr"]["name"] == attr_name:
                continue
            for sub_attr in artifact["sub_attr"]:
                if sub_attr["name"] == attr_name:
                    attr_name = None
                    break
            if not attr_name:
                continue
            attr_value = choices(attrs[attr_name]["sub"], sub_attr_value_weight)[0]
            artifact["sub_attr"].append({"name": attr_name, "value": attr_value})
            break
    else:
        sub_attr = choice(artifact["sub_attr"])
        attr_name = sub_attr["name"]
        attr_value = choices(attrs[attr_name]["sub"], sub_attr_value_weight)[0]
        sub_attr["value"] += attr_value
    return attr_name, attr_value


def enhance(artifact):
    ret = '强化:'
    while artifact["level"] < 20:
        artifact["level"] = (artifact["level"] // 4 + 1) * 4
        artifact["main_attr"]["value"] = attrs[artifact["main_attr"]["name"]]["main_20"]
        attr_name, attr_value = enhance_sub_attr(artifact)
        ret += f' {attrs[attr_name]["name"]}+{print_value(attr_value)}'
    return ret


def get_rand_artifact(suit_name=None):
    suit_name = suit_name if isinstance(suit_name, str) else choice(suit_name) if suit_name else choice(
        list(suit.keys()))
    slot_name = choice(list(slot.keys()))
    main_attr = choice(slot[slot_name]["main"])
    artifact = {
        "suit": suit_name,
        "slot": slot_name,
        "level": 0,
        "main_attr": {"name": main_attr, "value": attrs[main_attr]["main_0"]},
        "sub_attr": [],
    }
    attr_p = random()
    while attr_p < attr_rate[len(artifact["sub_attr"])]:
        enhance_sub_attr(artifact)
    return artifact


def print_value(value):
    return f'{value:{"d" if isinstance(value, int) else ".1%"}}'


def print_attr(attr):
    return f'{attrs[attr["name"]]["name"]}+{print_value(attr["value"])}'


def print_artifact(artifact):
    ret = ''
    ret += f'{suit[artifact["suit"]][artifact["slot"]]} +{artifact["level"]}\n'
    ret += f'{artifact["slot"]}\n'
    ret += f'{print_attr(artifact["main_attr"])}\n'
    ret += f'★★★★★\n'
    for attr in artifact["sub_attr"]:
        ret += f'· {print_attr(attr)}\n'
    ret += f'{artifact["suit"]}'
    return ret


def get_artifact_image(artifact):
    # 获取圣遗物图片，会返回一个image

    img = background.copy()

    name = suit[artifact["suit"]][artifact["slot"]]
    icon = Image.open(os.path.join(RES_PATH, name + '.png'))
    # icon = icon.resize((190, 190))
    # icon_a = icon.getchannel("A")  # 有的图alpha通道有问题，需要对alpha处理一下
    # icon_a = ImageMath.eval("convert(a*b/256, 'L')", a=icon_a, b=icon_a)
    img.paste(icon, (420 - icon.width // 2, 192 - icon.height // 2), icon)

    draw = ImageDraw.Draw(img)
    draw.text((32, 10), name, fill="#ffffff", font=ImageFont.truetype(ttf_path, size=37))
    draw.text((32, 79), artifact["slot"], fill="#ffffff", font=ImageFont.truetype(ttf_path, size=23))
    attr = artifact["main_attr"]
    draw.text((32, 171), attrs[attr["name"]]["name"], fill="#bfafa8", font=ImageFont.truetype(ttf_path, size=23))
    draw.text((32, 198), print_value(attr["value"]), fill="#ffffff", font=ImageFont.truetype(ttf_path, size=47))
    level = f'+{artifact["level"]}'
    w, h = draw.textsize(level, font=ImageFont.truetype(ttf_path, size=27))
    draw.text((64 - w // 2, 360 - h // 2), level, fill="#ffffff", font=ImageFont.truetype(ttf_path, size=27))
    x, y = 32, 401
    for attr in artifact["sub_attr"]:
        draw.text((x, y), f'·{print_attr(attr)}', fill="#495366", font=ImageFont.truetype(ttf_path, size=27))
        y += 43

    return img


def print_artifact_img_CQ(artifact):
    img = get_artifact_image(artifact)
    buf = BytesIO()
    img.save(buf, format='PNG')
    return f"[CQ:image,file=base64://{base64.b64encode(buf.getvalue()).decode()}]"


def parse_content(content):
    content = content.strip()
    target = {"dungeon": None, "suit": None, "slot": None, "main_attr": None, "sub_attr": []}
    is_sub_attr = False
    while content:
        if CONTENT_SUB_ATTR_PREFIX and not is_sub_attr and len(content) > len(CONTENT_SUB_ATTR_PREFIX) and \
                content.startswith(CONTENT_SUB_ATTR_PREFIX):
            if len(target["sub_attr"]) >= max_attr:
                raise ValueError(f'副词条最多只能有{max_attr}个: {content}')
            is_sub_attr = True
            content = content[len(CONTENT_SUB_ATTR_PREFIX):]
            continue
        ok = False
        for i in range(min(len(content), keyword_max_len), 0, -1):
            ret = keywords.get(content[:i])
            if ret:
                if is_sub_attr:
                    if ret.get("main_attr"):
                        target["sub_attr"].append(ret["main_attr"])
                        ok = True
                        is_sub_attr = False
                else:
                    for k, v in ret.items():
                        if target.get(k):
                            raise ValueError(f'重复关键词: {content[:i]}')
                        target[k] = v
                    ok = True
                if ok:
                    content = content[i:].strip()
                    break
        if not ok:
            raise ValueError(f'没有找到关键词: {CONTENT_SUB_ATTR_PREFIX if is_sub_attr else ""}{content}')

    if target["suit"]:
        dungeon_name = None
        for k, v in dungeon.items():
            if target["suit"] in v["reward"]:
                dungeon_name = k
                break
        if not target["dungeon"]:
            target["dungeon"] = dungeon_name
        elif target["dungeon"] != dungeon_name:
            raise ValueError(f'圣遗物套装与所刷取的秘境不符')
    if target["slot"] and target["main_attr"]:
        if not target["main_attr"].intersection(set(slot[target["slot"]]["main"])):
            raise ValueError(f'圣遗物位置的主属性不符')

    return target


def check_sub_attr(target, subs, target_idx=0, used_sub=0):
    if len(target) > len(subs):
        return False
    if target_idx >= len(target):
        return True
    for sub_idx, sub in enumerate(subs):
        if used_sub & 1 << sub_idx:
            continue
        if sub["name"] in target[target_idx]:
            if check_sub_attr(target, subs, target_idx + 1, used_sub | 1 << sub_idx):
                return True
    return False


def get_target_artifact(target, max_times=1000000):
    ok = False
    for times in range(max(max_times, 1)):
        artifact = get_rand_artifact(dungeon[target["dungeon"]]["reward"] if target["dungeon"] else None)
        if target["suit"] and target["suit"] != artifact["suit"]:
            continue
        if target["slot"] and target["slot"] != artifact["slot"]:
            continue
        if target["main_attr"] and artifact["main_attr"]["name"] not in target["main_attr"]:
            continue
        if target["sub_attr"] and not check_sub_attr(target["sub_attr"], artifact["sub_attr"]):
            continue
        ok = True
        break
    msg = f'刷取{target["dungeon"] if target["dungeon"] else ""}圣遗物{times + 1}次，'
    if not ok:
        msg += '还是没有获得指定圣遗物，做人要知足，拿着这个，凑合着用吧：\n'
    else:
        msg += '获得：\n'
    return artifact, msg


@sv.on_prefix(["圣遗物", "原神圣遗物"], only_to_me=True)
async def genshin_artifact(bot, ev):
    try:
        target = parse_content(ev.message.extract_plain_text())
    except Exception as e:
        await bot.send(ev, str(e))
        return
    artifact, msg = get_target_artifact(target)
    try:
        msg += print_artifact_img_CQ(artifact)
    except:
        msg += print_artifact(artifact)
    if AUTO_ENHANCE:
        msg += f'\n\n{enhance(artifact)}\n'
        try:
            msg += print_artifact_img_CQ(artifact)
        except:
            msg += print_artifact(artifact)
    await bot.send(ev, msg, at_sender=True)


if __name__ == '__main__':
    # main()

    test = {
        "suit": "平息鸣雷的尊者", "slot": "生之花", "level": 0, "main_attr": {"name": "生命值", "value": 717},
        "sub_attr": [{"name": "元素精通", "value": 19}, {"name": "暴击率", "value": .035}, {"name": "暴击伤害", "value": .078}],
    }
    print(print_artifact(test))
    enhance(test)
    print(print_artifact(test))

    test = get_rand_artifact()
    print(print_artifact(test))

    target = parse_content("魔女火伤杯副攻副攻副暴副暴")
    print(target)
    test, msg = get_target_artifact(target)
    print(msg)
    print(print_artifact(test))

    enhance(test)
    img = get_artifact_image(test)
    img.show()
    # img.save('out/'+suit[i][1][j]+'_v2.png', 'png')
