#!/usr/bin/env python3
"""Single source of truth for creature models, textures, weapons, item textures, lang.
Run: python3 tools/gen_assets.py   (writes into src/main/resources)"""
import json, os, random, zlib
from PIL import Image, ImageDraw, ImageFilter

MOD = "hyrulecreatures"
RES = os.path.join(os.path.dirname(__file__), "..", "src", "main", "resources")
A = os.path.join(RES, "assets", MOD)
RANKS = ["red", "blue", "black", "silver", "gold"]
RANK_JA = ["赤", "青", "黒", "銀", "金"]


def hexc(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def P(n, p, box, pose, rot=(0, 0, 0), c="skin", f=None, r=0):
    return dict(n=n, p=p, box=list(box), pose=list(pose), rot=list(rot), c=c, f=f or [], r=r)


# ---------------------------------------------------------------- species
def biped_legs(arm_w, arm_h, arm_x, leg_w, leg_h, leg_x, leg_y, shoulder_y=2):
    return [
        P("rightArm", None, (-arm_w + 1, -2, -arm_w / 2, arm_w, arm_h, arm_w), (-arm_x, shoulder_y, 0), c="skin", f=["hand"]),
        P("leftArm", None, (-1, -2, -arm_w / 2, arm_w, arm_h, arm_w), (arm_x, shoulder_y, 0), c="skin", f=["hand"]),
        P("rightLeg", None, (-leg_w / 2, 0, -leg_w / 2, leg_w, leg_h, leg_w), (-leg_x, leg_y, 0), c="skin2"),
        P("leftLeg", None, (-leg_w / 2, 0, -leg_w / 2, leg_w, leg_h, leg_w), (leg_x, leg_y, 0), c="skin2"),
    ]


import math


def spider_legs(n, attach_y, radius, th, l1, l2, off=0.0):
    out = []
    for i in range(n):
        a = i * 2 * math.pi / n + off; dx, dz = round(math.cos(a), 3), round(math.sin(a), 3)
        out.append(P(f"leg{i}", None, (-1.5, 0, -1.5, 3, l1, 3), (dx * radius, attach_y, dz * radius), (th * dz, 0, -th * dx), c="bone"))
        out.append(P(f"leg{i}b", f"leg{i}", (-1, 0, -1, 2, l2, 2), (0, l1, 0), (-th * dz, 0, th * dx), c="joint"))
    return out


def guardian_parts(legs=True):
    """BotW Guardian Stalker (compendium photo): wide flat copper shell, small turret head, thick bone-white legs splayed low."""
    parts = [
        P("body", None, (-12, -3, -12, 24, 7, 24), (0, 9, 0), f=["circuit"]),
        P("shell2", "body", (-9, -5, -9, 18, 2, 18), (0, 0, 0), c="skin2", f=["circuit"]),
        P("rim", "body", (-12.5, 3, -12.5, 25, 1, 25), (0, 0, 0), c="horn"),
        P("lobeL", "body", (9, -4, -5, 3, 4, 10), (0, 0, 0), c="skin2"), P("lobeR", "body", (-12, -4, -5, 3, 4, 10), (0, 0, 0), c="skin2"),
        P("head", "body", (-4, -7, -4, 8, 7, 8), (0, -5, -3), c="skin", f=["circuit"]),
        P("cap", "head", (-3, -3, -3, 6, 3, 6), (0, -7, 0), c="skin2"),
        P("crest", "head", (-1, -5, -2, 2, 2, 4), (0, -7, 0), c="horn"),
        P("eyeCyl", "head", (-3, -6, -7, 6, 5, 3), (0, 0, 0), c="skin2", f=["bigeye"]),
        P("eyeRing", "head", (-4, -7, -5, 8, 7, 1), (0, 0, 0), c="horn"),
    ]
    if legs:
        for i in range(8):
            a_ = i * math.pi / 4 + math.pi / 8; dx, dz = round(math.cos(a_), 3), round(math.sin(a_), 3); th = 1.2
            parts.append(P(f"leg{i}", None, (-2, 0, -2, 4, 9, 4), (dx * 11, 12, dz * 11), (th * dz, 0, -th * dx), c="bone"))
            parts.append(P(f"leg{i}b", f"leg{i}", (-1.5, 0, -1.5, 3, 9, 3), (0, 9, 0), (-th * dz * 0.9, 0, th * dx * 0.9), c="joint"))
    return parts


def scout_parts():
    """Guardian Scout (shrine): small copper dome, eye turret, 4 short legs, 2 arms for energy weapons."""
    return [
        P("body", None, (-7, -5, -7, 14, 9, 14), (0, 11, 0), f=["circuit"]),
        P("shell2", "body", (-5, -8, -5, 10, 3, 10), (0, 0, 0), c="skin2", f=["circuit"]),
        P("rim", "body", (-7.5, 2, -7.5, 15, 1, 15), (0, 0, 0), c="horn"),
        P("head", "body", (-4, -7, -4, 8, 7, 8), (0, -5, -1), c="skin", f=["circuit"]),
        P("eyeCyl", "head", (-3, -5, -7, 6, 5, 3), (0, 0, 0), c="skin2", f=["bigeye"]),
        P("rightArm", None, (-2, -1, -2, 4, 13, 4), (-9, 6, -2), c="bone", f=["circuit"]),
        P("leftArm", None, (-2, -1, -2, 4, 13, 4), (9, 6, -2), c="bone", f=["circuit"]),
    ] + spider_legs(4, 13, 6, 0.8, 6, 5.5, math.pi / 4)


SPECIES = {
    "bokoblin": dict(hunch=0.45, parts=[
        P("body", None, (-4, 0, -2, 8, 12, 4), (0, 3, 0)),
        P("belly", "body", (-4, 3, -5, 8, 8, 3), (0, 0, 0), c="belly"),
        P("loin", "body", (-4, 10, -2, 8, 4, 4), (0, 1, 0), c="cloth"),
        P("head", None, (-5, -9, -5, 10, 9, 9), (0, 3, -1), f=["eyes"]),
        P("snout", "head", (-2.5, -4, -8, 5, 4, 3), (0, 0, 0), c="nose", f=["nostrils"]),
        P("jaw", "head", (-2, 0, -7, 4, 1, 2), (0, -1, 0), c="nose"),
        P("horn", "head", (-1, -5, -1, 2, 5, 2), (0, -8, -2), (-0.25, 0, 0), c="horn"),
        P("earL", "head", (0, -2, -0.5, 10, 4, 1), (5, -5, 0), (0, 0, -0.2), c="skin2"),
        P("earR", "head", (-10, -2, -0.5, 10, 4, 1), (-5, -5, 0), (0, 0, 0.2), c="skin2"),
        P("wrapR", "rightArm", (-4.5, 7, -3, 6, 5, 6), (0, 0, 0), c="bandage", f=["stripes"]),
        P("wrapL", "leftArm", (-1.5, 7, -3, 6, 5, 6), (0, 0, 0), c="bandage", f=["stripes"]),
    ] + biped_legs(5, 14, 5.5, 5, 9, 2.5, 15, 5)),
    "moblin": dict(hunch=0.3, parts=[
        P("body", None, (-5, 0, -4, 10, 13, 8), (0, 0, 0)),
        P("belly", "body", (-4, 5, -5, 8, 6, 1), (0, 0, 0), c="belly"),
        P("loin", "body", (-5.5, 10, -4.5, 11, 5, 9), (0, 0, 0), c="cloth"),
        P("head", None, (-4.5, -8, -5, 9, 8, 9), (0, 0, -1), f=["eyes"]),
        P("snout", "head", (-2.5, -4, -10, 5, 4, 5), (0, 0, 0), c="nose", f=["nostrils"]),
        P("tuskL", "head", (0, -2, -1, 1, 4, 1), (2, -2, -9), (0.2, 0, 0), c="horn"),
        P("tuskR", "head", (-1, -2, -1, 1, 4, 1), (-2, -2, -9), (0.2, 0, 0), c="horn"),
        P("mane", "head", (-1.5, -3, -5, 3, 3, 10), (0, -8, 0), c="hair"),
        P("hornL", "head", (0, -6, -1, 2, 6, 2), (3, -8, -2), (0, 0, -0.35), c="horn"),
        P("hornR", "head", (-2, -6, -1, 2, 6, 2), (-3, -8, -2), (0, 0, 0.35), c="horn"),
        P("earL", "head", (0, -2, -0.5, 6, 3, 1), (4.5, -5, 0), (0, 0, -0.5), c="skin2"),
        P("earR", "head", (-6, -2, -0.5, 6, 3, 1), (-4.5, -5, 0), (0, 0, 0.5), c="skin2"),
        P("rightArm", None, (-4, -2, -2.5, 5, 17, 5), (-7.5, 2, 0), f=["hand"]),
        P("leftArm", None, (-1, -2, -2.5, 5, 17, 5), (7.5, 2, 0), f=["hand"]),
        P("wrapR", "rightArm", (-4.5, 8, -3, 6, 6, 6), (0, 0, 0), c="bandage", f=["stripes"]),
        P("wrapL", "leftArm", (-1.5, 8, -3, 6, 6, 6), (0, 0, 0), c="bandage", f=["stripes"]),
        P("rightLeg", None, (-2.5, 0, -2.5, 5, 11, 5), (-3, 13, 0), c="skin2"),
        P("leftLeg", None, (-2.5, 0, -2.5, 5, 11, 5), (3, 13, 0), c="skin2")]),
    "lizalfos": dict(hunch=0.4, parts=[
        P("body", None, (-4, 0, -3, 8, 12, 6), (0, 0, 0)),
        P("belly", "body", (-3, 1, -3.5, 6, 10, 1), (0, 0, 0), c="belly"),
        P("spine", "body", (-0.5, 0, 0, 1, 11, 3), (0, 0, 2), c="horn"),
        P("vest", "body", (-4.5, 1, -3.5, 9, 7, 7), (0, 0, 0), c="cloth"),
        P("head", None, (-3, -6, -3, 6, 6, 6), (0, 0, -1), f=["eyes_side"]),
        P("snout", "head", (-2, -3, -8, 4, 3, 5), (0, 0, 0), c="skin2", f=["nostrils"]),
        P("jaw", "head", (-1.5, 0, -7, 3, 1, 4), (0, -0.5, 0), c="belly"),
        P("hornL", "head", (0, -1.5, -1, 2, 3, 8), (3, -5, 1), (0.1, 0.5, -0.2), c="horn"),
        P("hornR", "head", (-2, -1.5, -1, 2, 3, 8), (-3, -5, 1), (0.1, -0.5, 0.2), c="horn"),
        P("frillL", "head", (0, -2, -0.5, 4, 4, 1), (3, -3, 2), (0, 0.5, -0.3), c="horn"),
        P("frillR", "head", (-4, -2, -0.5, 4, 4, 1), (-3, -3, 2), (0, -0.5, 0.3), c="horn"),
        P("tail1", "body", (-2, -2, 0, 4, 4, 5), (0, 10, 2), (0.5, 0, 0), c="skin2"),
        P("tail2", "tail1", (-1.5, -1.5, 0, 3, 3, 5), (0, 0, 5), (0.25, 0, 0), c="skin2"),
        P("tail3", "tail2", (-1, -1, 0, 2, 2, 5), (0, 0, 5), c="skin2"),
    ] + biped_legs(4, 13, 5.5, 4, 12, 2.2, 12)),
    "hinox": dict(hunch=0.3, parts=[
        P("body", None, (-8, 0, -6, 16, 14, 12), (0, 0, 0)),
        P("belly", "body", (-7, 4, -8, 14, 9, 2), (0, 0, 0), c="belly"),
        P("vest", "body", (-8.5, 0, -6.5, 17, 7, 13), (0, 0, 0), c="cloth", f=["stripes"]),
        P("loin", "body", (-8.5, 11, -6.5, 17, 5, 13), (0, 0, 0), c="cloth"),
        P("head", None, (-6, -10, -6, 12, 10, 11), (0, 1, -2), f=["bigeye"]),
        P("snout", "head", (-3, -4, -9, 6, 4, 3), (0, 0, 0), c="nose", f=["nostrils"]),
        P("brow", "head", (-5.5, -2, -6.5, 11, 2, 1), (0, -7, 0), c="hair"),
        P("earL", "head", (0, -3, -1, 9, 6, 1), (6, -5, 0), (0, 0, -0.35), c="skin2"),
        P("earR", "head", (-9, -3, -1, 9, 6, 1), (-6, -5, 0), (0, 0, 0.35), c="skin2"),
        P("knot", "head", (-2, -5, -2, 4, 5, 4), (0, -10, 0), c="hair"),
        P("rightArm", None, (-6, -2, -3, 7, 16, 7), (-10, 2, 0), f=["hand"]),
        P("leftArm", None, (-1, -2, -3, 7, 16, 7), (10, 2, 0), f=["hand"]),
        P("rightLeg", None, (-3.5, 0, -3.5, 7, 8, 7), (-4, 16, 0), c="skin2"),
        P("leftLeg", None, (-3.5, 0, -3.5, 7, 8, 7), (4, 16, 0), c="skin2")]),
    "talus": dict(hunch=0.1, parts=[
        P("body", None, (-9, 0, -6, 18, 10, 12), (0, 6, 0), c="skin2"),
        P("rock1", "body", (-6, -5, -4, 12, 5, 9), (0, 0, 0), c="skin"),
        P("rock2", "body", (2, -8, -2, 6, 4, 6), (0, 0, 0), c="skin2"),
        P("ore", "body", (-2, -9, 1, 4, 6, 4), (-2, 0, 2), c="horn"),
        P("ore2", "body", (-1, 6, 5, 3, 5, 3), (3, 0, 0), c="horn"),
        P("head", None, (-3, -3, -3, 6, 5, 6), (0, 6, -6), c="skin"),
        P("rightArm", None, (-6, -2, -3, 7, 17, 6), (-12, 6, 0), c="skin", f=["hand"]),
        P("leftArm", None, (-1, -2, -3, 7, 17, 6), (12, 6, 0), c="skin", f=["hand"]),
        P("rightLeg", None, (-3, 0, -3, 6, 8, 6), (-5, 16, 0), c="skin2"),
        P("leftLeg", None, (-3, 0, -3, 6, 8, 6), (5, 16, 0), c="skin2")]),
    "gibdo": dict(hunch=0.65, parts=[
        P("body", None, (-4, 0, -2, 8, 12, 4), (0, 0, 0)),
        P("wrap", "body", (-4.5, 2, -2.5, 9, 3, 5), (0, 0, 0), c="cloth"),
        P("wrap2", "body", (-4.5, 7, -2.5, 9, 3, 5), (0, 0, 0), c="cloth"),
        P("head", None, (-4, -8, -4, 8, 8, 8), (0, 0, -1), f=["eyes"]),
        P("jaw", "head", (-3, 0, -4, 6, 2, 3), (0, -1, 0), c="skin2")] + biped_legs(3, 14, 5, 4, 10, 2, 12)),
    "octorok": dict(hunch=0.0, parts=[
        P("body", None, (-6, 0, -6, 12, 11, 12), (0, 11, 0), f=["eyes"]),
        P("top", "body", (-4, -3, -4, 8, 3, 8), (0, 0, 0), c="skin2"),
        P("snout", "body", (-2, 3, -13, 4, 4, 7), (0, 0, 0), c="skin2", f=["nostrils"]),
        P("lip", "body", (-3, 2, -14, 6, 6, 2), (0, 0, 0), c="belly"),
        P("crest", "body", (-1, -7, -3, 2, 4, 6), (0, 0, 0), c="horn"),
        P("rightLeg", None, (-2, 0, -2, 4, 3, 4), (-4, 21, -1), c="skin2"),
        P("leftLeg", None, (-2, 0, -2, 4, 3, 4), (4, 21, -1), c="skin2"),
        P("legB1", None, (-2, 0, -2, 4, 3, 4), (-4, 21, 3), c="skin2"),
        P("legB2", None, (-2, 0, -2, 4, 3, 4), (4, 21, 3), c="skin2")]),
    "wizzrobe": dict(hunch=0.0, parts=[
        P("body", None, (-4, 0, -3, 8, 14, 6), (0, 8, 0), c="cloth"),
        P("hem", "body", (-5, 12, -4, 10, 3, 8), (0, 0, 0), c="cloth"),
        P("trim", "body", (-4.5, 6, -3.5, 9, 2, 7), (0, 0, 0), c="hair"),
        P("head", None, (-4, -8, -4, 8, 8, 8), (0, 8, 0), c="hair"),
        P("face", "head", (-3, -6, -4.5, 6, 5, 1), (0, 0, 0), c="belly", f=["eyes"]),
        P("cone", "head", (-3, -7, -3, 6, 7, 6), (0, -8, 0), c="hair"),
        P("tip", "head", (-1.5, -5, -1.5, 3, 5, 3), (0, -15, 0), (0.3, 0, 0), c="hair"),
        P("rightArm", None, (-3, -2, -2, 4, 10, 4), (-6, 10, 0), c="cloth", f=["hand"]),
        P("leftArm", None, (-1, -2, -2, 4, 10, 4), (6, 10, 0), c="cloth", f=["hand"])]),
    "lynel": dict(hunch=0.12, parts=[
        P("horse", None, (-6, 0, -3, 12, 11, 18), (0, 6, 0), c="skin2"),
        P("tail1", "horse", (-2, 0, 0, 4, 12, 3), (0, 1, 17), (0.3, 0, 0), c="hair"),
        P("body", None, (-5, -14, -4, 10, 14, 8), (0, 6, -1)),
        P("belly", "body", (-3.5, -9, -5, 7, 11, 1), (0, 0, 0), c="belly"),
        P("head", None, (-4, -8, -4, 8, 8, 8), (0, -8, -3), f=["eyes"]),
        P("snout", "head", (-2, -3, -7, 4, 3, 3), (0, 0, 0), c="skin2", f=["nostrils"]),
        P("mane", "head", (-2.5, -9, 2, 5, 17, 4), (0, 0, 0), c="hair"),
        P("hornL", "head", (0, -6, -1, 2, 7, 2), (3, -8, 0), (0, 0, -0.4), c="horn"),
        P("hornR", "head", (-2, -6, -1, 2, 7, 2), (-3, -8, 0), (0, 0, 0.4), c="horn"),
        P("rightArm", None, (-4, -2, -2.5, 5, 15, 5), (-7.5, -6, -2), f=["hand"]),
        P("leftArm", None, (-1, -2, -2.5, 5, 15, 5), (7.5, -6, -2), f=["hand"]),
        P("frontRightLeg", None, (-2.5, 0, -2.5, 5, 7, 5), (-4, 17, 0), c="skin2"),
        P("frontLeftLeg", None, (-2.5, 0, -2.5, 5, 7, 5), (4, 17, 0), c="skin2"),
        P("backRightLeg", None, (-2.5, 0, -2.5, 5, 7, 5), (-4, 17, 14), c="skin2"),
        P("backLeftLeg", None, (-2.5, 0, -2.5, 5, 7, 5), (4, 17, 14), c="skin2")]),
    "chuchu": dict(hunch=0.0, parts=[
        P("body", None, (-5, 0, -5, 10, 8, 10), (0, 16, 0)),
        P("core", "body", (-2, -2, -2, 4, 2, 4), (0, 0, 0), c="belly"),
        P("eyeL", "body", (0, -4, -3, 4, 5, 4), (1, 0, -1), c="horn", f=["bigeye"]),
        P("eyeR", "body", (-4, -4, -3, 4, 5, 4), (-1, 0, -1), c="horn", f=["bigeye"])]),
    "guardian": dict(hunch=0.0, parts=guardian_parts()),
    "keese": dict(hunch=0, parts=[
        P("body", None, (-3, -3, -3, 6, 6, 6), (0, 19, 0), f=["bigeye"]),
        P("earL", "body", (0, -3, -0.5, 2, 3, 1), (2, -3, -1), c="horn"),
        P("earR", "body", (-2, -3, -0.5, 2, 3, 1), (-2, -3, -1), c="horn"),
        P("wingL", "body", (0, -0.5, -4, 16, 1, 10), (3, -1, 0), c="wing"),
        P("wingR", "body", (-16, -0.5, -4, 16, 1, 10), (-3, -1, 0), c="wing"),
        P("footL", "body", (-0.5, 0, -0.5, 1, 3, 1), (1.5, 3, 0), c="horn"),
        P("footR", "body", (-0.5, 0, -0.5, 1, 3, 1), (-1.5, 3, 0), c="horn"),
    ]),
}

# palette per species, per rank: key -> hex ; tuples listed in RANKS order
def pal(skin, skin2, belly, cloth, horn, hair="#2a1f1a", wing="#201828", eye="#ffd23a"):
    return dict(skin=skin, skin2=skin2, belly=belly, cloth=cloth, horn=horn, hair=hair, wing=wing, eye=eye, bone=skin2, joint=horn, nose="#e8a0a8", bandage="#ece8d8")


PAL = {
    "bokoblin": [pal("#c8452f", "#a33322", "#e98a63", "#6b4a2b", "#e8dcb8"),
                 pal("#3f78c8", "#2d5aa0", "#8fb6e6", "#6b4a2b", "#e8dcb8"),
                 pal("#3a3547", "#27232f", "#6a6478", "#4a3a2b", "#c9c2a8"),
                 pal("#b9bfc9", "#8e95a3", "#e4e8ee", "#5d5d66", "#f2f2f2"),
                 pal("#e0b83a", "#b8912a", "#f6e08a", "#6b4a2b", "#fff2c0")],
    "moblin": [pal("#a4552f", "#7c3f22", "#d49a6a", "#5b4430", "#e8dcb8", "#3a2418"),
               pal("#3a6ba8", "#2a4f80", "#86a9d0", "#5b4430", "#e8dcb8", "#1c2a3e"),
               pal("#3c3a48", "#272530", "#6a6678", "#3f3226", "#c9c2a8", "#141418"),
               pal("#c4c8d0", "#989eaa", "#eceef2", "#55555e", "#ffffff", "#7a7f8c"),
               pal("#d9ad35", "#b08622", "#f4dc82", "#5b4430", "#fff2c0", "#8a6418")],
    "lizalfos": [pal("#5a9a3a", "#427a2a", "#e0d08a", "#6b4a2b", "#d8c15a", eye="#ff5a2a"),
                 pal("#3a8ac0", "#2a6a98", "#bfe0ee", "#6b4a2b", "#e8f0f6", eye="#ffee55"),
                 pal("#3a3a4a", "#28283a", "#8a8aa0", "#4a3a2b", "#aaaabb", eye="#ff3030"),
                 pal("#b8c4cc", "#8e9aa4", "#f0f4f6", "#5d5d66", "#ffffff", eye="#66ddff"),
                 pal("#e0b83a", "#b8912a", "#f8e8a0", "#6b4a2b", "#fff2c0", eye="#ffffff")],
    "keese": [pal("#3a3040", "#2a2030", "#5a4a60", "#000000", "#4a3a50", wing="#2a2236", eye="#ff4040"),
              pal("#8a2a22", "#661a18", "#c85a4a", "#000000", "#5a2a20", wing="#a8322a", eye="#ffd040"),
              pal("#3a68a8", "#2a4a80", "#8ab0e0", "#000000", "#2a4a70", wing="#6fa0dc", eye="#ffffff"),
              pal("#d0b020", "#a08418", "#f0e070", "#000000", "#706010", wing="#e8cc30", eye="#303030"),
              pal("#e0b83a", "#b8912a", "#f8e8a0", "#000000", "#fff2c0", wing="#ffe27a", eye="#ff3030")],
}

def setp(sid, name, box=None, pose=None, rot=None):
    for q in SPECIES[sid]["parts"]:
        if q["n"] == name:
            if box: q["box"] = list(box)
            if pose: q["pose"] = list(pose)
            if rot: q["rot"] = list(rot)
# --- shape corrections from compendium photo comparison ---
SPECIES["bokoblin"].update(hunch=0.7, splay=0.45, crouch=3)
setp("bokoblin", "head", pose=(0, 4, -3.5)); setp("bokoblin", "rightArm", pose=(-8, 5, 0)); setp("bokoblin", "leftArm", pose=(8, 5, 0))
SPECIES["moblin"].update(hunch=0.75, splay=0.1, crouch=1)
setp("moblin", "head", pose=(0, 2, -4)); setp("moblin", "rightArm", box=(-4, -2, -2.5, 5, 20, 5)); setp("moblin", "leftArm", box=(-1, -2, -2.5, 5, 20, 5))
setp("moblin", "hornL", box=(0, -10, -1, 2, 10, 2), rot=(-0.8, 0, -0.35)); setp("moblin", "hornR", box=(-2, -10, -1, 2, 10, 2), rot=(-0.8, 0, 0.35))
SPECIES["lizalfos"].update(hunch=0.8, splay=0.12, crouch=1)
setp("lizalfos", "rightArm", box=(-3, -2, -2, 4, 16, 4)); setp("lizalfos", "leftArm", box=(-1, -2, -2, 4, 16, 4))
SPECIES["hinox"].update(hunch=0.55, splay=0.2, crouch=2)
setp("hinox", "body", box=(-9, 0, -7, 18, 14, 14)); setp("hinox", "head", pose=(0, 5, -4)); setp("hinox", "rightArm", box=(-6, -2, -3, 7, 21, 7)); setp("hinox", "leftArm", box=(-1, -2, -3, 7, 21, 7))
SPECIES["lynel"].update(hunch=0.15)
setp("lynel", "body", box=(-7, -15, -5, 14, 15, 10)); setp("lynel", "belly", box=(-5, -10, -6, 10, 12, 1)); setp("lynel", "head", box=(-5, -9, -5, 10, 9, 10), pose=(0, -9, -3))
setp("lynel", "rightArm", box=(-5, -2, -3, 6, 15, 6), pose=(-9.5, -6, -2)); setp("lynel", "leftArm", box=(-1, -2, -3, 6, 15, 6), pose=(9.5, -6, -2))
SPECIES["wizzrobe"].update(hunch=0.0)
setp("wizzrobe", "body", box=(-6, 0, -4, 12, 14, 8)); setp("wizzrobe", "hem", box=(-8, 12, -5, 16, 3, 10)); setp("wizzrobe", "head", box=(-5, -8, -5, 10, 8, 10))
setp("wizzrobe", "cone", box=(-4, -5, -4, 8, 5, 8)); setp("wizzrobe", "tip", box=(-1.5, -4, -1.5, 3, 4, 3)); setp("wizzrobe", "body", box=(-7, 0, -5, 14, 14, 10)); setp("wizzrobe", "hem", box=(-10, 12, -6, 20, 3, 12))
setp("wizzrobe", "rightArm", box=(-3, -2, -3, 6, 12, 6), pose=(-9, 10, 0)); setp("wizzrobe", "leftArm", box=(-3, -2, -3, 6, 12, 6), pose=(9, 10, 0))
SPECIES["octorok"]["parts"] = [
    P("body", None, (-8, 0, -8, 16, 14, 16), (0, 8, 0), f=["eyes"]),
    P("balloon", "body", (-6, -7, -6, 12, 7, 12), (0, 0, 0), c="skin2"), P("knob", "body", (-1.5, -10, -1.5, 3, 3, 3), (0, 0, 0), c="horn"),
    P("snout", "body", (-2.5, 6, -15, 5, 5, 8), (0, 0, 0), c="skin2", f=["nostrils"]), P("lip", "body", (-3.5, 5, -16, 7, 7, 2), (0, 0, 0), c="belly"),
    P("rightLeg", None, (-2, 0, -2, 4, 3, 4), (-5, 21, -1), c="skin2"), P("leftLeg", None, (-2, 0, -2, 4, 3, 4), (5, 21, -1), c="skin2"),
    P("legB1", None, (-2, 0, -2, 4, 3, 4), (-5, 21, 4), c="skin2"), P("legB2", None, (-2, 0, -2, 4, 3, 4), (5, 21, 4), c="skin2")]
SPECIES["talus"]["parts"] = [
    P("body", None, (-11, 0, -8, 22, 10, 16), (0, 10, 0), c="skin2"),
    P("rock1", "body", (-8, -6, -6, 16, 6, 12), (0, 0, 0), c="skin"), P("rock2", "body", (2, -9, -3, 7, 4, 6), (0, 0, 0), c="skin2"),
    P("ore", "body", (-2, -11, 1, 4, 6, 4), (-2, 0, 2), c="horn"), P("ore2", "body", (-1, 6, 7, 3, 5, 3), (3, 0, 0), c="horn"),
    P("head", None, (-2, -2, -2, 4, 4, 4), (0, 12, -7), c="skin"),
    P("rightArm", None, (-5, -2, -4, 8, 12, 8), (-14, 10, 0), c="skin", f=["hand"]), P("leftArm", None, (-3, -2, -4, 8, 12, 8), (14, 10, 0), c="skin", f=["hand"]),
    P("rightLeg", None, (-4, 0, -4, 8, 6, 8), (-9, 18, -4), c="skin2"), P("leftLeg", None, (-4, 0, -4, 8, 6, 8), (9, 18, -4), c="skin2")]
SPECIES["talus"].update(hunch=0.0, splay=0.5)
setp("keese", "body", box=(-3.5, -3.5, -3.5, 7, 7, 7), pose=(0, 18, 0)); setp("keese", "wingL", box=(0, -0.5, -6, 22, 1, 13)); setp("keese", "wingR", box=(-22, -0.5, -6, 22, 1, 13))
setp("keese", "earL", box=(0, -5, -0.5, 3, 5, 1)); setp("keese", "earR", box=(-3, -5, -0.5, 3, 5, 1))
setp("chuchu", "body", box=(-8, 0, -8, 16, 7, 16), pose=(0, 17, 0)); setp("chuchu", "eyeL", box=(-2.5, -5, -2.5, 5, 5, 5), pose=(3.5, 0, -4)); setp("chuchu", "eyeR", box=(-2.5, -5, -2.5, 5, 5, 5), pose=(-3.5, 0, -4))
import copy
_h = copy.deepcopy(SPECIES["bokoblin"]); _h["hunch"] = 0.7
_h["parts"] = [q for q in _h["parts"] if q["n"] not in ("horn", "jaw", "wrapR", "wrapL", "belly")] + [
    P("jaw", "head", (-3, 0, -8, 6, 3, 6), (0, 1, 0), (0.5, 0, 0), c="nose"),
    P("teeth", "head", (-2.5, -0.5, -8, 5, 1, 1), (0, 0, 0), c="bandage"),
    P("ribs", "body", (-3.5, 1, -2.5, 7, 9, 1), (0, 0, 0), c="belly", f=["stripes"]),
    P("gloomA", "body", (-6, -3, -1, 5, 6, 5), (0, 0, 0), c="horn"),
    P("gloomB", "body", (1, -2, 0, 4, 5, 4), (0, 0, 0), c="horn"),
    P("gloomC", "head", (-3, -11, -2, 4, 4, 4), (0, 0, 0), c="horn"),
    P("tatterR", "rightArm", (-4.5, 6, -3, 6, 7, 6), (0, 0, 0), c="cloth", f=["stripes"]),
    P("tatterL", "leftArm", (-1.5, 6, -3, 6, 7, 6), (0, 0, 0), c="cloth", f=["stripes"])]
SPECIES["horriblin"] = _h
SPECIES["stalkoblin"] = SPECIES["bokoblin"]
SPECIES["stalmoblin"] = SPECIES["moblin"]
SPECIES["stalizalfos"] = SPECIES["lizalfos"]
SPECIES["yiga_footsoldier"] = dict(hunch=0.05, parts=[
    P("body", None, (-4, 0, -2, 8, 12, 4), (0, 0, 0)),
    P("belt", "body", (-4.5, 8, -2.5, 9, 2, 5), (0, 0, 0), c="cloth"),
    P("head", None, (-4, -8, -4, 8, 8, 8), (0, 0, 0), c="belly"),
    P("mask", "head", (-4.5, -8, -5, 9, 6, 1), (0, 0, 0), c="horn", f=["eyes"]),
    P("hood", "head", (-4.5, -9, -4.5, 9, 3, 9), (0, 0, 0), c="skin2"),
] + biped_legs(4, 12, 5, 4, 12, 2, 12))
SPECIES["yiga_blademaster"] = SPECIES["yiga_footsoldier"]
SPECIES["soldier_construct"] = dict(hunch=0.0, parts=[
    P("body", None, (-5, 0, -3, 10, 12, 6), (0, 0, 0)),
    P("core", "body", (-2, 3, -4, 4, 4, 1), (0, 0, 0), c="horn"),
    P("head", None, (-4, -7, -4, 8, 7, 8), (0, 0, 0), c="skin2", f=["bigeye"]),
    P("padL", "body", (0, -2, -3.5, 4, 2, 7), (4, 0, 0), c="horn"),
    P("padR", "body", (-4, -2, -3.5, 4, 2, 7), (-4, 0, 0), c="horn"),
] + biped_legs(5, 12, 7, 5, 12, 2.5, 12))
SPECIES["captain_construct"] = SPECIES["soldier_construct"]
SPECIES["blizzrobe"] = SPECIES["wizzrobe"]
SPECIES["thunder_wizzrobe"] = SPECIES["wizzrobe"]
SPECIES["decayed_guardian"] = SPECIES["guardian"]
for _n in (1, 2, 3, 4): SPECIES[f"guardian_scout_{_n}"] = dict(hunch=0.15, parts=scout_parts())
SPECIES["guardian_turret"] = dict(hunch=0.0, parts=[
    P("base", None, (-9, 0, -9, 18, 5, 18), (0, 19, 0), c="skin2", f=["circuit"]),
    P("body", None, (-8, -4, -8, 16, 8, 16), (0, 15, 0), f=["circuit"]),
    P("rim", "body", (-8.5, 2, -8.5, 17, 1, 17), (0, 0, 0), c="horn"),
    P("head", "body", (-5, -9, -5, 10, 9, 10), (0, -4, 0), c="skin", f=["circuit"]),
    P("crest", "head", (-1, -3, -2, 2, 3, 4), (0, -9, 0), c="horn"),
    P("eyeCyl", "head", (-3.5, -7, -8, 7, 6, 3), (0, 0, 0), c="skin2", f=["bigeye"])])
SPECIES["guardian_skywatcher"] = dict(hunch=0.0, parts=[
    P("body", None, (-4, -3, -4, 8, 6, 8), (0, 11, 0), f=["circuit"]),
    P("mast", "body", (-1, -9, -1, 2, 6, 2), (0, 0, 0), c="bone"),
    P("pod", "body", (-3, 3, -3, 6, 5, 6), (0, 0, 0), c="skin2", f=["circuit"]),
    P("eyeCyl", "body", (-2.5, 5, -6, 5, 4, 3), (0, 0, 0), c="skin2", f=["bigeye"]),
    P("armL", "body", (0, -1, -1, 9, 2, 2), (4, 0, 0), c="bone"),
    P("armR", "body", (-9, -1, -1, 9, 2, 2), (-4, 0, 0), c="bone"),
    P("wingL", "body", (0, -0.5, -2, 14, 1, 4), (0, -9, 0), c="horn"),
    P("wingR", "body", (-14, -0.5, -2, 14, 1, 4), (0, -9, 0), c="horn")])
SPECIES["frox"] = SPECIES["talus"]
SPECIES["stalhinox"] = SPECIES["hinox"]
SPECIES["calamity_ganon"] = dict(hunch=0.0, parts=guardian_parts() + [
    P("hornL", "body", (0, -14, -2, 3, 12, 3), (6, -4, 0), (0, 0, -0.5), c="horn"),
    P("hornR", "body", (-3, -14, -2, 3, 12, 3), (-6, -4, 0), (0, 0, 0.5), c="horn"),
    P("hornL2", "body", (0, -10, -2, 3, 9, 3), (9, -2, 2), (0, 0, -0.9), c="horn"),
    P("hornR2", "body", (-3, -10, -2, 3, 9, 3), (-9, -2, 2), (0, 0, 0.9), c="horn"),
    P("spk1", "body", (-1.5, -10, 2, 3, 8, 3), (0, 0, 0), (0.3, 0, 0), c="horn"),
    P("spk2", "body", (-1.5, -9, 6, 3, 8, 3), (0, 0, 0), (0.5, 0, 0), c="horn"),
    P("core", "body", (-3, 0, -9.5, 6, 6, 1), (0, 0, 0), c="horn")])
SPECIES["master_kohga"] = SPECIES["yiga_blademaster"]
BLIGHT = dict(hunch=0.15, parts=[
    P("body", None, (-5, 0, -3, 10, 14, 6), (0, 0, 0), c="cloth"),
    P("robe", "body", (-6.5, 9, -4.5, 13, 8, 9), (0, 0, 0), c="cloth"),
    P("cape", "body", (-6, 0, 2.5, 12, 20, 1), (0, 0, 0), c="skin2"),
    P("core", "body", (-2, 3, -3.5, 4, 4, 1), (0, 0, 0), c="horn"),
    P("head", None, (-4, -8, -4, 8, 8, 8), (0, 0, -0.5), c="skin2", f=["eyes"]),
    P("crown", "head", (-5, -3, -5, 10, 2, 10), (0, -8, 0), c="horn"),
    P("hornL", "head", (0, -7, -1, 2, 7, 2), (3, -8, 0), (0, 0, -0.35), c="horn"),
    P("hornR", "head", (-2, -7, -1, 2, 7, 2), (-3, -8, 0), (0, 0, 0.35), c="horn"),
    P("rightArm", None, (-4, -2, -2, 4, 17, 4), (-7, 2, 0), c="skin", f=["hand"]),
    P("leftArm", None, (0, -2, -2, 4, 17, 4), (7, 2, 0), c="skin", f=["hand"]),
    P("rightLeg", None, (-2.5, 0, -2.5, 5, 10, 5), (-2.5, 14, 0), c="skin2"),
    P("leftLeg", None, (-2.5, 0, -2.5, 5, 10, 5), (2.5, 14, 0), c="skin2")])
def blight_variant(extra):
    return dict(hunch=BLIGHT["hunch"], parts=[dict(q) for q in BLIGHT["parts"]] + extra)
SPECIES["fireblight_ganon"] = blight_variant([
    P("flame", "head", (-3, -8, -2, 6, 8, 4), (0, -8, 0), c="horn"),
    P("flameL", "head", (0, -6, -1, 3, 6, 3), (4, -8, 0), (0, 0, -0.5), c="horn"),
    P("flameR", "head", (-3, -6, -1, 3, 6, 3), (-4, -8, 0), (0, 0, 0.5), c="horn"),
    P("padL", "body", (0, -3, -4, 6, 4, 8), (5, 0, 0), c="horn"), P("padR", "body", (-6, -3, -4, 6, 4, 8), (-5, 0, 0), c="horn")])
SPECIES["waterblight_ganon"] = blight_variant([
    P("finL", "head", (0, -3, -0.5, 8, 6, 1), (4, -3, 0), (0, 0.4, -0.3), c="horn"),
    P("finR", "head", (-8, -3, -0.5, 8, 6, 1), (-4, -3, 0), (0, -0.4, 0.3), c="horn"),
    P("dorsal", "body", (-1, -4, 3, 2, 14, 3), (0, 0, 0), c="horn")])
SPECIES["windblight_ganon"] = blight_variant([
    P("wingL", "body", (0, -0.5, -2, 16, 1, 9), (4, 2, 4), c="cloth"),
    P("wingR", "body", (-16, -0.5, -2, 16, 1, 9), (-4, 2, 4), c="cloth"),
    P("scarf", "head", (-4.5, 0, -4.5, 9, 3, 9), (0, 0, 0), c="cloth")])
SPECIES["thunderblight_ganon"] = blight_variant([
    P("padL", "body", (0, -5, -5, 8, 6, 10), (4, 0, 0), c="cloth"), P("padR", "body", (-8, -5, -5, 8, 6, 10), (-4, 0, 0), c="cloth"),
    P("spikeL", "body", (0, -12, -1, 2, 8, 2), (8, -3, 0), (0, 0, -0.3), c="horn"), P("spikeR", "body", (-2, -12, -1, 2, 8, 2), (-8, -3, 0), (0, 0, 0.3), c="horn"),
    P("bolt", "head", (-1, -10, -1, 2, 6, 2), (0, -8, 0), c="horn")])
SPECIES["phantom_ganon"] = SPECIES["yiga_footsoldier"]
def gleeok_parts():
    parts = [
        P("body", None, (-7, 0, -9, 14, 11, 18), (0, 10, 0)),
        P("belly", "body", (-6, 8, -8, 12, 3, 16), (0, 0, 0), c="belly"),
        P("back", "body", (-1, -3, -6, 2, 3, 12), (0, 0, 0), c="horn"),
        P("tail1", "body", (-3, -2, 0, 6, 6, 8), (0, 4, 9), (0.25, 0, 0), c="skin2"),
        P("tail2", "tail1", (-2, -2, 0, 4, 4, 8), (0, 0, 8), c="skin2"),
        P("tail3", "tail2", (-1, -1, 0, 2, 2, 7), (0, 0, 8), c="horn"),
        P("footL", "body", (-2.5, 0, -2.5, 5, 9, 5), (4.5, 10, -4), c="skin2"),
        P("footR", "body", (-2.5, 0, -2.5, 5, 9, 5), (-4.5, 10, -4), c="skin2"),
        P("wingL", "body", (0, -0.5, -5, 20, 1, 13), (7, -1, -1), c="wing"),
        P("wingR", "body", (-20, -0.5, -5, 20, 1, 13), (-7, -1, -1), c="wing"),
        P("wbL", "body", (0, -1.5, -1, 20, 2, 2), (7, -1, -3), (0, 0, 0), c="skin2"),
        P("wbR", "body", (-20, -1.5, -1, 20, 2, 2), (-7, -1, -3), c="skin2"),
    ]
    for k, x, rz in (("L", 5, .35), ("M", 0, 0), ("R", -5, -.35)):
        parts += [
            P(f"neck{k}", "body", (-1.5, -24, -1.5, 3, 24, 3), (x, 2, -8), (-0.25, 0, rz * 1.4), c="skin2"),
            P(f"head{k}", f"neck{k}", (-3, -4, -7, 6, 5, 7), (0, -24, 0), (0.7, 0, 0), f=["eyes"]),
            P(f"snout{k}", f"head{k}", (-2, -3.5, -12, 4, 3, 5), (0, 0, 0), c="skin2", f=["nostrils"]),
            P(f"jaw{k}", f"head{k}", (-2, 0, -11, 4, 1, 4), (0, -0.5, 0), (0.25, 0, 0), c="belly"),
            P(f"hornA{k}", f"head{k}", (1.5, -7, -2, 1, 5, 1), (0, 0, 0), (0.4, 0, -0.2), c="horn"),
            P(f"hornB{k}", f"head{k}", (-2.5, -7, -2, 1, 5, 1), (0, 0, 0), (0.4, 0, 0.2), c="horn"),
        ]
    return parts


SPECIES["gleeok"] = dict(hunch=0.0, parts=gleeok_parts())

PAL["hinox"] = [pal("#7a5a8a", "#5a3f68", "#a98cb8", "#4a3a2b", "#e8dcb8", "#241a2a", eye="#ffe14a"),
                pal("#4a7ab0", "#35567e", "#8fb0d6", "#4a3a2b", "#e8dcb8", "#1c2a3e", eye="#ffe14a"),
                pal("#3a3a48", "#262632", "#6a6a7a", "#3a2a1b", "#c9c2a8", "#101018", eye="#ff4a3a"),
                pal("#b8c0c8", "#8e98a4", "#e8ecf0", "#55555e", "#ffffff", "#707888", eye="#66ddff"),
                pal("#d9ad35", "#b08622", "#f4dc82", "#5b4430", "#fff2c0", "#8a6418", eye="#ffffff")]
PAL["talus"] = [pal("#8a8478", "#6a6458", "#a8a294", "#000000", "#e0902a", eye="#ff7a2a"),
                pal("#7a8a98", "#5a6a78", "#9aaab8", "#000000", "#4ac0e8", eye="#aaffff"),
                pal("#4a4850", "#33313a", "#6a6870", "#000000", "#b04aff", eye="#ff4aff"),
                pal("#b8bcc4", "#9096a0", "#d8dce2", "#000000", "#ffffff", eye="#66ddff"),
                pal("#c4a040", "#9a7c2a", "#e4cc7a", "#000000", "#fff2c0", eye="#ffffff")]
PAL["gibdo"] = [pal("#b8a888", "#8f8068", "#d8cba8", "#d8d0b8", "#e8e0c8", eye="#ff3030"),
                pal("#8aa0b0", "#687d8c", "#b0c4d0", "#c8d4dc", "#e8e0c8", eye="#40e0ff"),
                pal("#6a5a70", "#4c3f52", "#8a7a90", "#a89cae", "#e8e0c8", eye="#ff40ff"),
                pal("#c8ccd0", "#a0a4a8", "#e8eaec", "#f0f0f0", "#ffffff", eye="#66ffcc"),
                pal("#d8b860", "#b0903f", "#f0d890", "#f0e4b0", "#fff2c0", eye="#ffffff")]
PAL["horriblin"] = [pal("#8a9a78", "#667856", "#b4c4a0", "#4a4030", "#d8d0b0", eye="#ff3030"),
                    pal("#7a98a8", "#587684", "#a8c4d0", "#4a4030", "#d8d0b0", eye="#40e0ff"),
                    pal("#5a4a6a", "#403350", "#8a7a9a", "#3a3028", "#c0b8a0", eye="#ff40ff"),
                    pal("#c0c8c4", "#98a09c", "#e4e8e6", "#55555e", "#ffffff", eye="#66ffcc"),
                    pal("#d8b860", "#b0903f", "#f0d890", "#5b4430", "#fff2c0", eye="#ffffff")]

PAL["octorok"] = [pal("#c8452f", "#a33322", "#e98a63", "#000000", "#e8dcb8", eye="#ffffff"),
                  pal("#3f78c8", "#2d5aa0", "#8fb6e6", "#000000", "#e8dcb8", eye="#ffffff"),
                  pal("#3a3547", "#27232f", "#6a6478", "#000000", "#c9c2a8", eye="#ffee55"),
                  pal("#b9bfc9", "#8e95a3", "#e4e8ee", "#000000", "#f2f2f2", eye="#66ddff"),
                  pal("#e0b83a", "#b8912a", "#f6e08a", "#000000", "#fff2c0", eye="#ffffff")]
# wizzrobe: fire, ice, electric, meteo, gold
PAL["wizzrobe"] = [pal("#d9b48a", "#b08a62", "#d9b48a", "#9a2a1e", "#e8dcb8", hair="#c8452f", eye="#ff6a2a"),
                   pal("#d9b48a", "#b08a62", "#d9b48a", "#2a5aa8", "#e8dcb8", hair="#3f78c8", eye="#aaffff"),
                   pal("#d9b48a", "#b08a62", "#d9b48a", "#8a7a1e", "#e8dcb8", hair="#d8c030", eye="#ffff66"),
                   pal("#d9b48a", "#b08a62", "#d9b48a", "#4a3a5a", "#e8dcb8", hair="#7a4aa8", eye="#ff66ff"),
                   pal("#d9b48a", "#b08a62", "#d9b48a", "#8a6a1e", "#e8dcb8", hair="#e0b83a", eye="#ffffff")]

PAL["lynel"] = [pal("#c89a5a", "#a07a42", "#e8c890", "#8a4a3a", "#e8dcb8", "#b8402a"),
                pal("#7a9ac0", "#5a789c", "#b4cce0", "#3a6aa8", "#e8dcb8", "#2a4a8a"),
                pal("#4a3a3a", "#33292a", "#7a6a6a", "#2a2a34", "#c9c2a8", "#e8e0d0"),
                pal("#d8dce0", "#b0b4b8", "#f4f6f8", "#8e98a4", "#ffffff", "#ffffff"),
                pal("#e0b83a", "#b8912a", "#f6e08a", "#e8c85a", "#fff2c0", "#fff2a0")]
PAL["chuchu"] = [pal("#d84a30", "#a83020", "#ff8a60", "#000000", "#ffd060", eye="#ffffff"),
                 pal("#3f88e0", "#2a64b0", "#8ac0ff", "#000000", "#c0f0ff", eye="#ffffff"),
                 pal("#6a4a8a", "#4a3266", "#9a7ab8", "#000000", "#e0a0ff", eye="#ffffff"),
                 pal("#e8ecf0", "#c0c4c8", "#ffffff", "#000000", "#a0e0ff", eye="#202020"),
                 pal("#e8c830", "#b8a020", "#fff080", "#000000", "#ffffff", eye="#ffffff")]
def anc(shell, shell2, head, glow, eye, bone="#d8d0b8", joint="#6a9a78"):
    d = pal(shell, shell2, head, "#000000", glow, eye=eye); d["bone"] = bone; d["joint"] = joint; return d
PAL["guardian"] = [anc("#8a4a3e", "#6a3228", "#7a4036", "#ff4a9a", "#40c8ff"),
                   anc("#4a6a90", "#34506e", "#40607e", "#40e0ff", "#a0f0ff", joint="#4a8aa8"),
                   anc("#3a3638", "#242022", "#302c2e", "#ff3a3a", "#ff7050", bone="#bcb4a4", joint="#7a4a4a"),
                   anc("#b8b4a8", "#908c80", "#a8a498", "#40ffb0", "#80ffd0", bone="#ece8dc", joint="#8ab89a"),
                   anc("#b09040", "#887028", "#a08034", "#fff0a0", "#ffffff", bone="#e8d8a8", joint="#c0a050")]
for _sid in ("guardian_turret", "guardian_skywatcher", "guardian_scout_1", "guardian_scout_2", "guardian_scout_3", "guardian_scout_4"):
    PAL[_sid] = PAL["guardian"]
PAL["decayed_guardian"] = [anc("#5a6a44", "#3e4a2e", "#4e5e3a", "#d8408a", "#60c0ff", bone="#b8b494", joint="#506a40"),
                           anc("#4a6a58", "#34503e", "#3e5e4a", "#60e0c0", "#a0f0ff", bone="#b0b8a0", joint="#406a58"),
                           anc("#4a4a40", "#30302a", "#40403a", "#e05030", "#ff8050", bone="#a8a290", joint="#605040"),
                           anc("#8a9078", "#686e58", "#7a8068", "#a0e090", "#c0ffb0", bone="#d0d0b8", joint="#789068"),
                           anc("#8a7a40", "#685a2c", "#7a6c38", "#e8c860", "#ffe890", bone="#d8c898", joint="#a08a48")]

def bone(eye):
    d = pal("#e6e0cc", "#c4bca4", "#d0c8b0", "#bfb79c", "#f4f0e0", eye=eye); d["nose"] = "#c4bca4"; return d
for _sid, _src, _eye in (("stalkoblin", "bokoblin", "#66ccff"), ("stalmoblin", "moblin", "#66ccff"), ("stalizalfos", "lizalfos", "#66ccff")):
    PAL[_sid] = [bone(_eye), bone("#aaddff"), bone("#ff66ff"), bone("#ffffff"), bone("#ffe066")]
def suit(a, b, mask): return pal(a, b, "#d9b48a", "#000000", mask, hair=b, eye="#ff3030")
PAL["yiga_footsoldier"] = [suit("#8a1e1e", "#5a1212", "#e8e0d0"), suit("#2a2a3a", "#161622", "#e8e0d0"),
                           suit("#3a1e5a", "#241238", "#e8e0d0"), suit("#6a6a74", "#44444c", "#ffffff"), suit("#a08a2a", "#6a5a18", "#fff2c0")]
PAL["yiga_blademaster"] = [suit("#5a1212", "#2e0808", "#c8c0b0"), suit("#161622", "#0a0a10", "#c8c0b0"),
                           suit("#241238", "#120820", "#c8c0b0"), suit("#44444c", "#26262c", "#e0e0e0"), suit("#6a5a18", "#3a300c", "#e8d890")]
def cons(a, b, glow): return pal(a, b, a, "#000000", "#707882", eye=glow)
PAL["soldier_construct"] = [cons("#8a948c", "#6a746c", "#40e0ff"), cons("#7a8a9c", "#5a6a7c", "#40ffa0"),
                            cons("#5a5a66", "#3c3c46", "#ff8a30"), cons("#b8c0c8", "#8e969e", "#ffffff"), cons("#c0a860", "#98803e", "#fff2a0")]
PAL["captain_construct"] = PAL["soldier_construct"]

PAL["frox"] = [pal("#7a8470", "#5a6454", "#9aa490", "#000000", "#e0902a", eye="#ff7a2a"), pal("#6a8aa0", "#4a6a80", "#8aaac0", "#000000", "#4ac0e8", eye="#aaffff"),
               pal("#3f4048", "#2a2b32", "#5a5c66", "#000000", "#b04aff", eye="#ff4aff"), pal("#b8bcc4", "#9096a0", "#d8dce2", "#000000", "#ffffff", eye="#66ddff"),
               pal("#c4a040", "#9a7c2a", "#e4cc7a", "#000000", "#fff2c0", eye="#ffffff")]
PAL["phantom_ganon"] = [suit("#3a4a5a", "#222c38", "#cfe8ff"), suit("#2a4a6a", "#162a40", "#cfe8ff"), suit("#2a2a3a", "#12121c", "#cfe8ff"),
                        suit("#8a9aaa", "#5a6672", "#ffffff"), suit("#8a7a3a", "#5a4e22", "#fff2c0")]
def drag(a, b, w): return pal(a, b, "#e8d8b0", "#000000", "#e8dcb8", wing=w, eye="#ffee55")
PAL["gleeok"] = [drag("#a83a2a", "#7a2418", "#c84a30"), drag("#3a78b8", "#2a5688", "#4a90d0"), drag("#d8c030", "#a89020", "#e8d848"),
                 drag("#a8b4c0", "#808c98", "#c8d4e0"), drag("#d8a838", "#a88222", "#e8c458")]

for _p in PAL["bokoblin"]: _p["eye"] = "#46c8ff"

def setp(sid, i, **kw): PAL[sid][i].update(kw)
# --- tuned against in-game compendium photos (rank 0 = the common look) ---
PAL["keese"][0] = pal("#6a4a34", "#4a3224", "#8a6a4e", "#000000", "#5a3a28", wing="#7a5a40", eye="#ffd030")
PAL["hinox"][0] = pal("#a24a3a", "#7c3428", "#c88068", "#5a4030", "#e8dcb8", "#ece8dc", eye="#ffe14a")
PAL["talus"][0] = pal("#a8a090", "#858070", "#c4bcaa", "#000000", "#e8902a", eye="#ff7a2a")
PAL["octorok"][0] = pal("#8a8a92", "#686870", "#c8c8d0", "#000000", "#e8dcb8", eye="#ffffff")
PAL["octorok"][1] = pal("#3f78c8", "#2d5aa0", "#8fb6e6", "#000000", "#e8dcb8", eye="#ffffff")
PAL["octorok"][2] = pal("#5a8a3a", "#406a28", "#98c070", "#000000", "#e8dcb8", eye="#ffffff")
PAL["octorok"][3] = pal("#e8ecf0", "#c0c4c8", "#ffffff", "#000000", "#a0e0ff", eye="#303030")
for i, (robe, hood, eye) in enumerate((("#e8dcc0", "#b83a2a", "#ff6a2a"), ("#e8e4d8", "#3a70c0", "#aaffff"), ("#e8e0b8", "#c8b020", "#ffff66"),
                                     ("#d8d0e0", "#7a4aa8", "#ff66ff"), ("#f0e4b8", "#d8a838", "#ffffff"))):
    PAL["wizzrobe"][i] = pal("#d9b48a", "#b08a62", "#241a1a", robe, "#e8dcb8", hair=hood, eye=eye)
PAL["lynel"][0] = pal("#6a4a38", "#4a3226", "#8a6a50", "#4a3a30", "#e8dcb8", "#b02a20")
PAL["chuchu"][0] = pal("#58b0f0", "#3a88c8", "#a8d8ff", "#000000", "#ff8a20", eye="#202020")
PAL["moblin"][0] = pal("#9a3a30", "#722a22", "#d49a7a", "#5b4430", "#e8dcb8", "#3a2418")
PAL["lizalfos"][0] = pal("#4a9a3a", "#357828", "#e0d08a", "#7a8a68", "#e8dcb8", eye="#ffd030")
PAL["bokoblin"][0].update(skin="#e0522c", skin2="#b83a20", belly="#f0a070")

PAL["stalhinox"] = [bone("#66ccff"), bone("#aaddff"), bone("#ff66ff"), bone("#ffffff"), bone("#ffe066")]
PAL["master_kohga"] = PAL["yiga_blademaster"]
PAL["calamity_ganon"] = [anc("#2a2430", "#1a141e", "#3a2c3a", "#ff2a2a", "#ffd040", bone="#4a3a4a", joint="#8a1a1a")] * 5
def blight(robe, glow):
    return pal("#2e2428", "#1c1418", "#d9b48a", robe, glow, eye=glow)
PAL["fireblight_ganon"] = [blight("#7a2418", "#ff7a20")] * 5
PAL["waterblight_ganon"] = [blight("#1f4a7a", "#40d0ff")] * 5
PAL["windblight_ganon"] = [blight("#3f6a52", "#d0ffd0")] * 5
PAL["thunderblight_ganon"] = [blight("#6a5a1a", "#ffee40")] * 5

# --- second reference pass (TotK compendium photos) ---
PAL["hinox"][0] = pal("#6f7d66", "#566350", "#8a9680", "#8a5a38", "#e8dcb8", "#e8e4d4", eye="#b070e0")
PAL["hinox"][1] = pal("#5a7a8a", "#43606e", "#7a98a6", "#6a4a30", "#e8dcb8", "#cfd8e0", eye="#e8a030")
PAL["hinox"][2] = pal("#4a4a4e", "#34343a", "#6a6a70", "#503828", "#c9c2a8", "#b8b8b8", eye="#ff6030")
for _i, _p in enumerate(PAL["hinox"]): _p["nose"] = "#c8909a"
PAL["talus"][0] = pal("#d8d0b8", "#b0a890", "#e8e0c8", "#000000", "#4ae0a0", eye="#4ae0a0")
PAL["talus"][1] = pal("#5a5a5a", "#3e3e3e", "#7a7a7a", "#000000", "#4ae0a0", eye="#4ae0a0")
PAL["talus"][2] = pal("#e4e4e0", "#bcbcb8", "#f4f4f0", "#000000", "#a0e0ff", eye="#a0e0ff")
PAL["talus"][3] = pal("#4a3a30", "#2e2420", "#6a4a38", "#000000", "#ff9a20", eye="#ff9a20")
PAL["talus"][4] = pal("#c8e4f4", "#9ac0d8", "#e8f4fc", "#000000", "#e0f8ff", eye="#e0f8ff")
PAL["lynel"][0] = pal("#6a604a", "#4a4234", "#a04a3a", "#4a3a30", "#e8dcb8", "#a02a20")
PAL["lynel"][1] = pal("#7a708a", "#5a5068", "#6a5a90", "#4a3a50", "#e8dcb8", "#3a5aa0")
PAL["lynel"][2] = pal("#7a7468", "#5a5448", "#8a8a8a", "#4a4440", "#e8dcb8", "#e8e8f0")
PAL["phantom_ganon"] = [suit("#5a1a14", "#2a0a08", "#c03020")] * 5
def cons2(glow): return pal("#5a8a78", "#3a6a58", "#5a8a78", "#000000", "#707882", eye=glow)
PAL["soldier_construct"] = [cons2("#40ffc0"), cons2("#80ffe0"), cons2("#ff8a30"), cons2("#ffffff"), cons2("#fff2a0")]
PAL["captain_construct"] = PAL["soldier_construct"]

def horri(skin, gloom, eye="#ff2a2a"):
    return pal(skin, "#4a4a42", "#7a7a68", "#2a2420", gloom, eye=eye)
PAL["horriblin"] = [horri("#8a8a74", "#a01818"), horri("#7a8a98", "#7a18a0"), horri("#5a5a62", "#a01860"), horri("#b8bcb0", "#c04020"), horri("#c0a860", "#d02020")]
for _p in PAL["horriblin"]: _p["nose"] = "#6a5a50"
# --- elemental variants
for _id, _src in (("lizalfos_fire", "lizalfos"), ("lizalfos_ice", "lizalfos"), ("lizalfos_elec", "lizalfos"),
                  ("keese_fire", "keese"), ("keese_ice", "keese"), ("keese_elec", "keese")):
    SPECIES[_id] = SPECIES[_src]
def tint(base, skin, skin2, belly, horn):
    d = dict(base); d.update(skin=skin, skin2=skin2, belly=belly, horn=horn); return d
_el = {"fire": ("#d8602a", "#a84418", "#f0b070", "#ff7a20", "#ff6a20"), "ice": ("#7ab8d8", "#5a98b8", "#e0f0f8", "#bfe8ff", "#60d8ff"),
       "elec": ("#d8c030", "#a89020", "#f8f0a0", "#fff040", "#ffee40")}
for _k, (_sk, _s2, _bl, _hn, _ey) in _el.items():
    PAL["lizalfos_" + _k] = [tint(PAL["lizalfos"][i], _sk, _s2, _bl, _hn) for i in range(5)]
    for _p in PAL["lizalfos_" + _k]: _p["eye"] = _ey
    PAL["keese_" + _k] = [dict(tint(PAL["keese"][i], _s2, _sk, _bl, _hn), wing=_sk, eye=_ey) for i in range(5)]
# chuchu: 0 normal, 1 fire, 2 ice, 3 electric, 4 gold(rare)
PAL["chuchu"] = [pal("#58b0f0", "#3a88c8", "#a8d8ff", "#000000", "#ff8a20", eye="#202020"),
                 pal("#e0502a", "#b03418", "#ff9a70", "#000000", "#ff8a20", eye="#202020"),
                 pal("#d8f0ff", "#a8d0e8", "#ffffff", "#000000", "#ff8a20", eye="#202020"),
                 pal("#f0d838", "#c8b020", "#fff8a0", "#000000", "#ff8a20", eye="#202020"),
                 pal("#e8c830", "#b8a020", "#fff080", "#000000", "#ff4a20", eye="#202020")]

for _k, _rows in (("blizzrobe", (("#f0f4f8", "#9ad8f8", "#aaffff"), ("#e8f0f8", "#6aa8e8", "#ccffff"), ("#dce8f4", "#4a78c8", "#88ddff"), ("#f4f8ff", "#c8e8ff", "#ffffff"), ("#f0ecd8", "#a8d0e8", "#ffffff"))),
                  ("thunder_wizzrobe", (("#e8e0b0", "#d8c020", "#ffff66"), ("#e0dcc0", "#c8a818", "#ffee44"), ("#d8d0a0", "#a88810", "#ffff88"), ("#f0ecd0", "#e8d848", "#ffffff"), ("#f0e4a8", "#e8b820", "#ffffff")))):
    PAL[_k] = [pal("#d9b48a", "#b08a62", "#241a1a", r, "#e8dcb8", hair=h, eye=e) for (r, h, e) in _rows]

def _rc(hexs, f):
    r, g, b = hexc(hexs); r, g, b = f(r, g, b); return "#%02x%02x%02x" % (max(0, min(255, int(r))), max(0, min(255, int(g))), max(0, min(255, int(b))))
def ranks5(base):
    """derive 5 rank palettes from one: orig, blue-swap, dark, pale, gold-tinted"""
    fs = [lambda r, g, b: (r, g, b), lambda r, g, b: (b, g * 0.95, r), lambda r, g, b: (r * .5, g * .5, b * .55),
          lambda r, g, b: (r * .45 + 140, g * .45 + 140, b * .45 + 145), lambda r, g, b: (r * .55 + 100, g * .55 + 80, b * .55 + 20)]
    out = []
    for f in fs:
        d = {k: (v if k in ("eye",) else _rc(v, f)) for k, v in base.items()}
        out.append(d)
    return out

# ================= Skyward Sword creatures =================
SPECIES["stalfos"] = dict(hunch=0.3, parts=[
    P("body", None, (-4, 0, -2, 8, 12, 4), (0, 0, 0), c="skin2"),
    P("ribs", "body", (-4.5, 1, -2.5, 9, 8, 5), (0, 0, 0), c="skin", f=["stripes"]),
    P("pelvis", "body", (-4, 10, -2, 8, 3, 4), (0, 0, 0), c="cloth"),
    P("head", None, (-4, -8, -4, 8, 8, 8), (0, 0, -1), c="skin", f=["eyes"]),
    P("helm", "head", (-4.5, -9, -4.5, 9, 4, 9), (0, 0, 0), c="horn"),
    P("hornL", "head", (0, -5, -1, 2, 5, 2), (4, -8, 0), (0, 0, -0.5), c="horn"),
    P("hornR", "head", (-2, -5, -1, 2, 5, 2), (-4, -8, 0), (0, 0, 0.5), c="horn"),
    P("jaw", "head", (-3, 0, -4, 6, 2, 4), (0, -1, 0), c="skin2"),
] + biped_legs(3, 13, 4.5, 3, 12, 2, 12))
SPECIES["stalmaster"] = dict(hunch=0.3, parts=[q for q in SPECIES["stalfos"]["parts"]] + [
    P("padL", "body", (0, -3, -3.5, 5, 4, 7), (4, 0, 0), c="cloth"), P("padR", "body", (-5, -3, -3.5, 5, 4, 7), (-4, 0, 0), c="cloth"),
    P("cape", "body", (-5, 0, 2.5, 10, 20, 1), (0, 0, 0), c="cloth"),
    P("arm3", "body", (-4, -1, -2, 3, 12, 3), (-6, 6, 0), (0, 0, 0.5), c="skin"), P("arm4", "body", (1, -1, -2, 3, 12, 3), (6, 6, 0), (0, 0, -0.5), c="skin")])
SPECIES["dark_lizalfos"] = SPECIES["lizalfos"]
SPECIES["armos"] = dict(hunch=0.15, parts=[
    P("body", None, (-6, 0, -4, 12, 14, 8), (0, 0, 0), f=["circuit"]),
    P("chest", "body", (-4, 3, -5, 8, 6, 1), (0, 0, 0), c="horn"),
    P("head", None, (-4.5, -8, -4.5, 9, 8, 9), (0, 0, -1), c="skin2", f=["eyes"]),
    P("visor", "head", (-4, -5, -5, 8, 2, 1), (0, 0, 0), c="horn"),
    P("crest", "head", (-1, -4, -4, 2, 4, 8), (0, -8, 0), c="skin"),
    P("rightArm", None, (-5, -2, -3, 6, 15, 6), (-9, 2, 0), c="skin2", f=["hand"]),
    P("leftArm", None, (-1, -2, -3, 6, 15, 6), (9, 2, 0), c="skin2", f=["hand"]),
    P("rightLeg", None, (-3, 0, -3, 6, 10, 6), (-3.5, 14, 0), c="skin"), P("leftLeg", None, (-3, 0, -3, 6, 10, 6), (3.5, 14, 0), c="skin")])
SPECIES["beamos"] = dict(hunch=0.0, parts=[
    P("base", None, (-7, 0, -7, 14, 4, 14), (0, 20, 0), c="skin2", f=["circuit"]),
    P("body", None, (-4, 0, -4, 8, 14, 8), (0, 8, 0), f=["circuit"]),
    P("head", None, (-7, -7, -7, 14, 14, 14), (0, 4, 0), c="skin2", f=["bigeye"]),
    P("ringL", "head", (7, -3, -3, 2, 6, 6), (0, 0, 0), c="horn"), P("ringR", "head", (-9, -3, -3, 2, 6, 6), (0, 0, 0), c="horn"),
    P("crest", "head", (-1, -10, -3, 2, 3, 6), (0, 0, 0), c="horn")])
SPECIES["skulltula"] = dict(hunch=0.0, parts=[
    P("body", None, (-5, -4, -6, 10, 8, 12), (0, 17, 0), c="skin"),
    P("head", None, (-3.5, -3.5, -6, 7, 7, 6), (0, 17, -6), c="skin2", f=["eyes"]),
    P("fangL", "head", (0, 2, -6.5, 1, 4, 1), (1.5, 0, 0), c="bandage"), P("fangR", "head", (-1, 2, -6.5, 1, 4, 1), (-1.5, 0, 0), c="bandage"),
    P("mark", "body", (-2, -4.5, 0, 4, 1, 5), (0, 0, 0), c="horn")] + spider_legs(8, 17, 4, 1.15, 6, 6, math.pi / 8))
SPECIES["deku_baba"] = dict(hunch=0.0, parts=[
    P("body", None, (-1.5, 0, -1.5, 3, 16, 3), (0, 8, 0), c="skin2"),
    P("leafL", "body", (0, 8, -1, 7, 1, 4), (1.5, 0, 0), (0, 0, -0.4), c="skin2"), P("leafR", "body", (-7, 8, -1, 7, 1, 4), (-1.5, 0, 0), (0, 0, 0.4), c="skin2"),
    P("head", None, (-5, -5, -5, 10, 8, 10), (0, 7, 0), c="skin", f=["eyes"]),
    P("jaw", "head", (-4, 3, -9, 8, 3, 8), (0, 0, 0), c="belly"),
    P("lip", "head", (-4.5, -1, -9.5, 9, 2, 5), (0, 0, 0), c="horn"),
    P("teeth", "head", (-3.5, 2, -9, 7, 1, 1), (0, 0, 0), c="bandage"),
    P("petal", "head", (-1, -9, -1, 2, 4, 2), (0, 0, 0), c="horn")])
_cb = [dict(q) for q in SPECIES["horriblin"]["parts"] if q["n"] not in ("ribs", "tatterR", "tatterL")]
SPECIES["cursed_bokoblin"] = dict(hunch=0.55, parts=_cb + [P("aura", "body", (-5, -1, -3, 10, 14, 6), (0, 0, 0), c="horn")])
SPECIES["ghirahim"] = dict(hunch=0.0, parts=[
    P("body", None, (-4, 0, -2.5, 8, 14, 5), (0, 0, 0), c="cloth"),
    P("collar", "body", (-6, -2, -3, 12, 4, 6), (0, 0, 0), c="horn"),
    P("diamond", "body", (-2, 4, -3, 4, 4, 1), (0, 0, 0), c="horn"),
    P("cape", "body", (-6, -1, 2.5, 12, 26, 1), (0, 0, 0), c="cloth"),
    P("head", None, (-4, -8, -4, 8, 8, 8), (0, 0, -0.5), c="skin", f=["eyes"]),
    P("hair", "head", (-4.5, -9, -4.5, 9, 3, 9), (0, 0, 0), c="hair"),
    P("spike", "head", (-1.5, -6, 3, 3, 6, 3), (0, -4, 0), (0.5, 0, 0), c="hair"),
] + biped_legs(3, 15, 5.5, 4, 12, 2, 14))
SPECIES["demise"] = dict(hunch=0.25, parts=[
    P("body", None, (-8, 0, -5, 16, 16, 10), (0, 0, 0), c="cloth"),
    P("chest", "body", (-6, 3, -6, 12, 8, 1), (0, 0, 0), c="horn"),
    P("padL", "body", (0, -4, -6, 9, 6, 12), (7, 0, 0), c="skin2"), P("padR", "body", (-9, -4, -6, 9, 6, 12), (-7, 0, 0), c="skin2"),
    P("head", None, (-5, -10, -5, 10, 10, 10), (0, 0, -1), c="skin", f=["eyes"]),
    P("mane", "head", (-6, -12, -2, 12, 14, 6), (0, 0, 0), c="hair"),
    P("hornL", "head", (0, -9, -1, 3, 9, 3), (4, -10, 0), (0, 0, -0.5), c="horn"), P("hornR", "head", (-3, -9, -1, 3, 9, 3), (-4, -10, 0), (0, 0, 0.5), c="horn"),
    P("rightArm", None, (-6, -2, -3, 7, 18, 7), (-11, 2, 0), c="skin", f=["hand"]), P("leftArm", None, (-1, -2, -3, 7, 18, 7), (11, 2, 0), c="skin", f=["hand"]),
    P("rightLeg", None, (-4, 0, -4, 8, 10, 8), (-4.5, 14, 0), c="skin2"), P("leftLeg", None, (-4, 0, -4, 8, 10, 8), (4.5, 14, 0), c="skin2")])
SPECIES["moldarach"] = dict(hunch=0.0, parts=[
    P("body", None, (-8, -4, -10, 16, 9, 20), (0, 16, 0), c="skin"),
    P("shell", "body", (-6, -7, -7, 12, 3, 14), (0, 0, 0), c="skin2", f=["circuit"]),
    P("head", None, (-4, -4, -5, 8, 7, 6), (0, 15, -10), c="skin2", f=["eyes"]),
    P("rightArm", None, (-3, -2, -9, 6, 4, 10), (-10, 14, -8), c="skin2"), P("leftArm", None, (-3, -2, -9, 6, 4, 10), (10, 14, -8), c="skin2"),
    P("clawR", "rightArm", (-4, -3, -14, 8, 6, 5), (0, 0, 0), c="horn"), P("clawL", "leftArm", (-4, -3, -14, 8, 6, 5), (0, 0, 0), c="horn"),
    P("tail1", "body", (-2.5, -2.5, 0, 5, 5, 8), (0, -1, 10), (-0.5, 0, 0), c="skin"),
    P("tail2", "tail1", (-2, -2, 0, 4, 4, 8), (0, 0, 8), (-0.5, 0, 0), c="skin"),
    P("tail3", "tail2", (-3, -3, 0, 6, 6, 6), (0, 0, 8), (-0.5, 0, 0), c="horn")] + spider_legs(8, 18, 6, 1.0, 5, 5, math.pi / 8))
SPECIES["koloktos"] = dict(hunch=0.0, parts=[
    P("body", None, (-7, 0, -5, 14, 16, 10), (0, 0, 0), f=["circuit"]),
    P("core", "body", (-3, 5, -6, 6, 6, 1), (0, 0, 0), c="horn"),
    P("head", None, (-5, -9, -5, 10, 9, 10), (0, 0, -1), c="skin2", f=["bigeye"]),
    P("crown", "head", (-6, -12, -6, 12, 3, 12), (0, 0, 0), c="horn"),
    P("rightArm", None, (-5, -2, -3, 6, 18, 6), (-10, 2, 0), c="skin2"), P("leftArm", None, (-1, -2, -3, 6, 18, 6), (10, 2, 0), c="skin2"),
    P("arm3", "body", (-4, -1, -3, 5, 16, 5), (-10, 8, 2), (0, 0, 0.5), c="skin2"), P("arm4", "body", (-1, -1, -3, 5, 16, 5), (10, 8, 2), (0, 0, -0.5), c="skin2"),
    P("arm5", "body", (-4, -1, -3, 5, 14, 5), (-9, 12, 3), (0, 0, 0.9), c="skin2"), P("arm6", "body", (-1, -1, -3, 5, 14, 5), (9, 12, 3), (0, 0, -0.9), c="skin2"),
    P("rightLeg", None, (-3.5, 0, -3.5, 7, 10, 7), (-4, 14, 0), c="skin"), P("leftLeg", None, (-3.5, 0, -3.5, 7, 10, 7), (4, 14, 0), c="skin")])
SPECIES["scaldera"] = dict(hunch=0.0, parts=[
    P("body", None, (-9, -6, -9, 18, 12, 18), (0, 14, 0), c="skin", f=["circuit"]),
    P("magma", "body", (-7, -8, -7, 14, 3, 14), (0, 0, 0), c="horn"),
    P("head", None, (-5, -5, -6, 10, 8, 8), (0, 13, -9), c="skin2", f=["eyes"]),
    P("rightArm", None, (-4, -2, -6, 8, 6, 10), (-11, 13, -5), c="skin2"), P("leftArm", None, (-4, -2, -6, 8, 6, 10), (11, 13, -5), c="skin2"),
    P("hornL", "head", (0, -8, -1, 3, 8, 3), (3, -5, -3), (0, 0, -0.4), c="horn"), P("hornR", "head", (-3, -8, -1, 3, 8, 3), (-3, -5, -3), (0, 0, 0.4), c="horn")]
    + spider_legs(8, 18, 7, 0.9, 4, 4, math.pi / 8))
SPECIES["the_imprisoned"] = dict(hunch=0.2, parts=[
    P("body", None, (-10, 0, -8, 20, 22, 16), (0, 0, 0)),
    P("belly", "body", (-8, 6, -9, 16, 12, 2), (0, 0, 0), c="belly"),
    P("head", None, (-7, -12, -7, 14, 12, 14), (0, 0, -2), c="skin", f=["bigeye"]),
    P("horn", "head", (-2, -16, -2, 4, 16, 4), (0, -12, -1), (0.2, 0, 0), c="horn"),
    P("jaw", "head", (-6, 0, -9, 12, 4, 8), (0, -1, 0), c="belly"),
    P("rightArm", None, (-7, -2, -4, 9, 22, 9), (-15, 2, 0), c="skin2", f=["hand"]), P("leftArm", None, (-2, -2, -4, 9, 22, 9), (15, 2, 0), c="skin2", f=["hand"]),
    P("rightLeg", None, (-5, 0, -5, 10, 8, 10), (-6, 22, 0), c="skin2"), P("leftLeg", None, (-5, 0, -5, 10, 8, 10), (6, 22, 0), c="skin2")])

SPECIES["tentalus"] = dict(hunch=0.0, parts=[
    P("body", None, (-9, -9, -9, 18, 14, 18), (0, 12, 0), c="skin"),
    P("head", None, (-7, -8, -7, 14, 9, 12), (0, 9, -2), c="skin2", f=["bigeye"]),
    P("crest", "head", (-1, -11, -3, 2, 4, 6), (0, 0, 0), c="horn"),
    P("spotL", "body", (4, -10, -3, 4, 1, 4), (0, 0, 0), c="horn"), P("spotR", "body", (-8, -10, -3, 4, 1, 4), (0, 0, 0), c="horn")]
    + spider_legs(8, 12, 7, 0.8, 6, 6, math.pi / 8))
import copy as _cp
SPECIES["techno_bokoblin"] = _cp.deepcopy(SPECIES["bokoblin"])
SPECIES["quadro_baba"] = _cp.deepcopy(SPECIES["deku_baba"])
SPECIES["quadro_baba"]["parts"] += [P(f"petal{i}", "head", (-1.5, -7, -1, 3, 8, 2), (dx * 4, -2, dz * 4), (dz * 0.8, 0, -dx * 0.8), c="horn")
                                    for i, (dx, dz) in enumerate(((1, 0), (-1, 0), (0, 1), (0, -1)))]
SPECIES["keese_dark"] = SPECIES["keese"]
SPECIES["wall_skulltula"] = SPECIES["skulltula"]
SPECIES["petit_moldorm"] = dict(hunch=0.0, parts=[
    P("body", None, (-3, -2.5, -4, 6, 5, 8), (0, 20, 0), c="skin"),
    P("head", None, (-2.5, -2.5, -4, 5, 5, 4), (0, 20, -4), c="skin2", f=["eyes"]),
    P("tail1", "body", (-2, -2, 0, 4, 4, 5), (0, 0, 4), c="skin2"), P("tail2", "tail1", (-1.5, -1.5, 0, 3, 3, 5), (0, 0, 5), c="skin2")]
    + spider_legs(6, 20, 3, 1.0, 3, 3, 0.3))
SPECIES["shakomite"] = dict(hunch=0.0, parts=[
    P("body", None, (-5, -4, -6, 10, 8, 10), (0, 18, 0), c="skin2"),
    P("shell", "body", (-7, -11, -2, 14, 12, 14), (0, 0, 2), c="skin", f=["circuit"]),
    P("head", None, (-3, -3, -5, 6, 6, 5), (0, 17, -6), c="skin2", f=["eyes"]),
    P("rightArm", None, (-3, -2, -8, 6, 4, 8), (-7, 18, -5), c="horn"), P("leftArm", None, (-3, -2, -8, 6, 4, 8), (7, 18, -5), c="horn")]
    + spider_legs(8, 20, 5, 0.9, 3, 3, math.pi / 8))
SPECIES["frog"] = dict(hunch=0.0, parts=[
    P("body", None, (-5, -4, -6, 10, 7, 12), (0, 19, 0), c="skin"),
    P("head", None, (-4.5, -3.5, -5, 9, 6, 6), (0, 19, -6), c="skin2", f=["nostrils"]),
    P("eyeL", "head", (0, -6, -3, 4, 4, 4), (1, 0, 0), c="horn", f=["bigeye"]), P("eyeR", "head", (-4, -6, -3, 4, 4, 4), (-1, 0, 0), c="horn", f=["bigeye"]),
    P("rightLeg", None, (-2, 0, -3, 4, 5, 6), (-5, 19, 4), c="skin2"), P("leftLeg", None, (-2, 0, -3, 4, 5, 6), (5, 19, 4), c="skin2")])
for _n in ("frog_magma", "frog_elec", "frog_dark", "frog_water"): SPECIES[_n] = SPECIES["frog"]
del SPECIES["frog"]
SPECIES["don_gerar"] = dict(hunch=0.15, parts=[
    P("body", None, (-5, 0, -3, 10, 14, 6), (0, 0, 0), c="skin"),
    P("belt", "body", (-5.5, 9, -3.5, 11, 2, 7), (0, 0, 0), c="horn"),
    P("coat", "body", (-6, 8, -4, 12, 8, 8), (0, 0, 0), c="cloth"),
    P("head", None, (-4, -8, -4, 8, 8, 8), (0, 0, -1), c="skin2", f=["eyes"]),
    P("hat", "head", (-6, -3, -6, 12, 2, 12), (0, -8, 0), c="cloth"), P("hatTop", "head", (-4, -6, -4, 8, 4, 8), (0, -9, 0), c="cloth"),
    P("rightArm", None, (-4, -2, -2, 4, 15, 4), (-7, 2, 0), c="skin", f=["hand"]),
    P("leftArm", None, (0, -2, -2, 4, 13, 4), (7, 2, 0), c="skin"), P("hook", "leftArm", (1, 10, -1, 1.5, 8, 1.5), (0, 0, 0), c="horn")]
    + [P("rightLeg", None, (-2.5, 0, -2.5, 5, 10, 5), (-2.5, 14, 0), c="skin2"), P("leftLeg", None, (-2.5, 0, -2.5, 5, 10, 5), (2.5, 14, 0), c="skin2")])
SPECIES["don_killer"] = SPECIES["don_gerar"]
SPECIES["gumarm"] = dict(hunch=0.0, parts=[
    P("body", None, (-8, -3, -8, 16, 7, 14), (0, 20, 2), c="skin", f=["circuit"]),
    P("head", None, (-1, -1, -1, 2, 2, 2), (0, 19, -8), c="skin2")]
    + [P(f"finger{i}", "body", (-1.8, -2, -12, 3.6, 5, 12), (x, 0, -7), (0, 0.12 * (i - 2), 0), c="skin2") for i, x in enumerate((-6, -3, 0, 3, 6))]
    + [P("thumb", "body", (-1.8, -2, -9, 3.6, 5, 9), (-8, 0, -2), (0, 0.9, 0), c="skin2")])
SPECIES["paraspalas"] = dict(hunch=0.0, parts=[
    P("body", None, (-8, -8, -8, 16, 16, 16), (0, 12, 0), f=["circuit"]),
    P("eyeCyl", "body", (-5, -5, -11, 10, 10, 3), (0, 0, 0), c="skin2", f=["bigeye"]),
    P("wingL", "body", (0, -0.5, -4, 14, 1, 10), (8, -2, 0), c="skin2"), P("wingR", "body", (-14, -0.5, -4, 14, 1, 10), (-8, -2, 0), c="skin2"),
    P("footL", "body", (-1.5, 0, -1.5, 3, 12, 3), (3, 8, 0), c="skin2"), P("footR", "body", (-1.5, 0, -1.5, 3, 12, 3), (-3, 8, 0), c="skin2"),
    P("footM", "body", (-1.5, 0, -1.5, 3, 14, 3), (0, 8, -4), c="skin2")])
# ================= Twilight Princess creatures =================
def quad(body, head, legs_y, leg_w, leg_h, front_z, back_z, lx, extra=()):
    n = [P("body", None, body, (0, legs_y, 0)), P("head", None, head[0], head[1], f=["eyes"])]
    for nm, (x, z) in (("frontRightLeg", (-lx, front_z)), ("frontLeftLeg", (lx, front_z)), ("backRightLeg", (-lx, back_z)), ("backLeftLeg", (lx, back_z))):
        n.append(P(nm, None, (-leg_w / 2, 0, -leg_w / 2, leg_w, leg_h, leg_w), (x, legs_y + body[1] + body[4], z), c="skin2"))
    return n + list(extra)
import copy as _cp2
SPECIES["bulblin"] = _cp2.deepcopy(SPECIES["moblin"])
SPECIES["king_bulblin"] = _cp2.deepcopy(SPECIES["moblin"])
SPECIES["king_bulblin"]["parts"] += [P("crown", "head", (-5, -3, -5.5, 10, 3, 10), (0, -8, 0), c="horn"), P("cape", "body", (-6, 0, 3.5, 12, 18, 1), (0, 0, 0), c="cloth")]
SPECIES["stalhound"] = dict(hunch=0.0, parts=quad((-4, -4, -8, 8, 8, 16), ((-3.5, -3.5, -6, 7, 7, 6), (0, 13, -9)), 14, 3, 6, -5, 6, 3.5, [
    P("snout", "head", (-1.5, 0, -9, 3, 2, 3), (0, 0, 0), c="skin2"), P("earL", "head", (1.5, -6, 0, 2, 3, 1), (0, 0, 0), c="skin"), P("earR", "head", (-3.5, -6, 0, 2, 3, 1), (0, 0, 0), c="skin"),
    P("ribs", "body", (-4.5, -3, -6, 9, 7, 10), (0, 0, 0), c="belly", f=["stripes"]), P("tail1", "body", (-1, -1, 0, 2, 2, 8), (0, -2, 8), (-0.5, 0, 0), c="skin2")]))
SPECIES["shadow_beast"] = dict(hunch=0.0, parts=quad((-5, -5, -9, 10, 10, 18), ((-4.5, -4.5, -7, 9, 9, 7), (0, 12, -10)), 14, 4, 6, -6, 7, 4, [
    P("spikeA", "body", (-1.5, -9, -6, 3, 5, 3), (0, 0, 0), c="horn"), P("spikeB", "body", (-1.5, -9, -1, 3, 6, 3), (0, 0, 0), c="horn"), P("spikeC", "body", (-1.5, -9, 4, 3, 5, 3), (0, 0, 0), c="horn"),
    P("hornL", "head", (1, -8, -2, 2, 5, 2), (0, 0, 0), c="horn"), P("hornR", "head", (-3, -8, -2, 2, 5, 2), (0, 0, 0), c="horn"), P("snout", "head", (-2, 0, -10, 4, 3, 3), (0, 0, 0), c="skin2")]))
SPECIES["redead"] = _cp2.deepcopy(SPECIES["gibdo"])
SPECIES["poe"] = dict(hunch=0.0, parts=[
    P("body", None, (-4, -5, -3, 8, 12, 6), (0, 15, 0), c="cloth"),
    P("hem", "body", (-5, 5, -4, 10, 3, 8), (0, 0, 0), c="cloth"),
    P("head", None, (-4, -8, -4, 8, 8, 8), (0, 10, -1), c="skin", f=["eyes"]), P("hood", "head", (-4.5, -9, -4.5, 9, 4, 9), (0, 0, 0), c="cloth"),
    P("rightArm", None, (-2, -1, -2, 3, 10, 3), (-6, 12, 0), c="skin2"), P("leftArm", None, (-1, -1, -2, 3, 10, 3), (6, 12, 0), c="skin2"),
    P("lantern", "rightArm", (-3, 9, -3, 6, 6, 6), (0, 0, 0), c="horn")])
SPECIES["tektite"] = dict(hunch=0.0, parts=[
    P("body", None, (-4, -3, -4, 8, 6, 8), (0, 16, 0), c="skin"), P("head", None, (-3, -3, -3, 6, 6, 4), (0, 16, -4), c="skin2", f=["eyes"]),
    P("eyeBig", "body", (-2, -5, -2, 4, 2, 4), (0, 0, 0), c="horn")] + spider_legs(4, 18, 4, 0.5, 5, 5, math.pi / 4))
SPECIES["peahat"] = dict(hunch=0.0, parts=[
    P("body", None, (-5, -5, -5, 10, 10, 10), (0, 14, 0), c="skin", f=["eyes"]),
    P("mouth", "body", (-3, 0, -6, 6, 3, 2), (0, 0, 0), c="horn"),
    P("wingL", "body", (0, -0.5, -2, 17, 1, 4), (0, -6, 0), c="skin2"), P("wingR", "body", (-17, -0.5, -2, 17, 1, 4), (0, -6, 0), c="skin2"),
    P("rootL", "body", (-1, 5, -1, 2, 6, 2), (3, 0, 0), c="skin2"), P("rootR", "body", (-1, 5, -1, 2, 6, 2), (-3, 0, 0), c="skin2")])
SPECIES["bubble_fire"] = dict(hunch=0.0, parts=[
    P("body", None, (-4, -4, -4, 8, 8, 8), (0, 16, 0), f=["eyes"]), P("jaw", "body", (-3, 3, -4, 6, 2, 4), (0, 0, 0), c="skin2"),
    P("flameA", "body", (-2, -8, -2, 4, 5, 4), (0, 0, 0), c="horn"), P("flameB", "body", (-5, -6, -1, 3, 4, 3), (0, 0, 0), c="horn"), P("flameC", "body", (2, -6, -1, 3, 4, 3), (0, 0, 0), c="horn")])
SPECIES["bubble_ice"] = SPECIES["bubble_fire"]; SPECIES["bubble_dark"] = SPECIES["bubble_fire"]
SPECIES["dodongo"] = dict(hunch=0.0, parts=quad((-7, -6, -12, 14, 12, 24), ((-5, -4.5, -9, 10, 9, 9), (0, 8, -12)), 12, 5, 6, -7, 8, 5, [
    P("jaw", "head", (-4, 3, -8, 8, 2, 8), (0, 0, 0), c="belly"), P("hornA", "head", (-1, -8, -4, 2, 4, 2), (0, 0, 0), c="horn"), P("hornB", "head", (-1, -8, 1, 2, 4, 2), (0, 0, 0), c="horn"),
    P("tail1", "body", (-3, -3, 0, 6, 6, 8), (0, 0, 12), c="skin"), P("tail2", "tail1", (-2, -2, 0, 4, 4, 8), (0, 0, 8), c="skin2"),
    P("spikes", "body", (-3, -9, -8, 6, 3, 16), (0, 0, 0), c="horn")]))
SPECIES["helmasaur"] = dict(hunch=0.0, parts=quad((-8, -3, -8, 16, 6, 16), ((-3, -3, -4, 6, 6, 5), (0, 16, -8)), 16, 4, 4, -6, 6, 6, [
    P("mask", "body", (-6, -8, -9, 12, 10, 2), (0, 0, 0), c="horn", f=["circuit"]), P("crestA", "mask", (-1, -4, 0, 2, 4, 2), (0, 0, 0), c="skin2")]))
SPECIES["dark_nut"] = dict(hunch=0.0, parts=[
    P("body", None, (-6, 0, -4, 12, 14, 8), (0, 0, 0), c="skin", f=["circuit"]),
    P("belt", "body", (-6.5, 10, -4.5, 13, 3, 9), (0, 0, 0), c="horn"),
    P("padL", "body", (0, -3, -5, 7, 5, 10), (6, 0, 0), c="skin2"), P("padR", "body", (-7, -3, -5, 7, 5, 10), (-6, 0, 0), c="skin2"),
    P("head", None, (-4.5, -9, -4.5, 9, 9, 9), (0, 0, -1), c="skin2", f=["eyes"]),
    P("hornL", "head", (0, -6, -1, 2, 7, 2), (4, -9, 0), (0, 0, -0.5), c="horn"), P("hornR", "head", (-2, -6, -1, 2, 7, 2), (-4, -9, 0), (0, 0, 0.5), c="horn"),
    P("plume", "head", (-1, -4, -1, 2, 12, 5), (0, -9, 2), c="cloth"),
    P("rightArm", None, (-5, -2, -3, 6, 16, 6), (-9, 2, 0), c="skin2", f=["hand"]), P("leftArm", None, (-1, -2, -3, 6, 16, 6), (9, 2, 0), c="skin2", f=["hand"]),
    P("rightLeg", None, (-3, 0, -3, 6, 10, 6), (-3.5, 14, 0), c="skin"), P("leftLeg", None, (-3, 0, -3, 6, 10, 6), (3.5, 14, 0), c="skin")])
SPECIES["death_sword"] = _cp2.deepcopy(SPECIES["stalfos"]); SPECIES["death_sword"]["parts"] += [P("cape", "body", (-6, -2, 2.5, 12, 24, 1), (0, 0, 0), c="cloth"), P("padL", "body", (0, -3, -3.5, 6, 4, 7), (4, 0, 0), c="cloth"), P("padR", "body", (-6, -3, -3.5, 6, 4, 7), (-4, 0, 0), c="cloth")]
SPECIES["zant"] = dict(hunch=0.1, parts=[
    P("body", None, (-4, 0, -2.5, 8, 14, 5), (0, 0, 0), c="cloth"), P("robe", "body", (-6, 8, -4, 12, 10, 8), (0, 0, 0), c="cloth"),
    P("collar", "body", (-6, -2, -3, 12, 4, 6), (0, 0, 0), c="horn"),
    P("head", None, (-4, -8, -4, 8, 8, 8), (0, 0, -0.5), c="skin", f=["eyes"]),
    P("helm", "head", (-6, -5, -6, 12, 4, 12), (0, -8, 0), c="skin2"),
    P("spikeN", "helm", (-1, -8, -6, 2, 8, 2), (0, 0, 0), (0, 0, 0), c="horn"), P("spikeL", "helm", (4, -7, -1, 2, 7, 2), (0, 0, 0), (0, 0, -0.5), c="horn"), P("spikeR", "helm", (-6, -7, -1, 2, 7, 2), (0, 0, 0), (0, 0, 0.5), c="horn"),
    P("rightArm", None, (-4, -2, -2, 4, 14, 4), (-7, 2, 0), c="cloth", f=["hand"]), P("leftArm", None, (0, -2, -2, 4, 14, 4), (7, 2, 0), c="cloth", f=["hand"])])
SPECIES["ganondorf"] = _cp2.deepcopy(SPECIES["demise"])
SPECIES["ganondorf"]["parts"] = [q for q in SPECIES["ganondorf"]["parts"] if q["n"] not in ("hornL", "hornR", "mane")] + [P("hair", "head", (-5, -11, -4, 10, 5, 9), (0, 0, 0), c="hair"), P("brow", "head", (-5, -6, -5.5, 10, 2, 1), (0, 0, 0), c="hair"), P("cape", "body", (-8, 0, 4.5, 16, 24, 1), (0, 0, 0), c="cloth")]
_g = gleeok_parts()
SPECIES["diababa"] = dict(hunch=0.0, parts=[q for q in _g if not q["n"].startswith(("wing", "wb", "tail", "foot"))] + [P("root1", "body", (-4, 8, -4, 8, 6, 8), (0, 0, 0), c="skin2")])
SPECIES["argorok"] = dict(hunch=0.0, parts=[q for q in _g if not any(q["n"].endswith(k) for k in ("L", "R")) or q["n"].startswith(("wing", "wb", "foot"))])
SPECIES["fyrus"] = _cp2.deepcopy(SPECIES["soldier_construct"])
SPECIES["fyrus"]["parts"] += [P("horn", "head", (-1.5, -8, -1, 3, 8, 3), (0, -7, 0), c="horn"), P("beard", "head", (-3, 0, -4.5, 6, 6, 1), (0, 0, 0), c="hair"), P("padL2", "body", (0, -4, -4, 6, 4, 8), (5, 0, 0), c="horn"), P("padR2", "body", (-6, -4, -4, 6, 4, 8), (-5, 0, 0), c="horn")]
SPECIES["armogohma"] = dict(hunch=0.0, parts=[
    P("body", None, (-8, -4, -9, 16, 8, 18), (0, 15, 0), c="skin"), P("head", None, (-3, -3, -4, 6, 6, 5), (0, 14, -9), c="skin2", f=["eyes"]),
    P("eyeball", "body", (-5, -9, -4, 10, 6, 10), (0, 0, 0), c="belly", f=["bigeye"]), P("pupil", "body", (-2, -10, -2, 4, 2, 4), (0, 0, 0), c="horn")] + spider_legs(8, 17, 6, 1.0, 6, 6, math.pi / 8))
SPECIES["aeralfos"] = _cp2.deepcopy(SPECIES["lizalfos"])
SPECIES["aeralfos"]["parts"] = [q for q in SPECIES["aeralfos"]["parts"] if q["n"] not in ("rightLeg", "leftLeg")] + [
    P("wingL", "body", (0, -0.5, -3, 18, 1, 12), (4, 3, 3), c="wing"), P("wingR", "body", (-18, -0.5, -3, 18, 1, 12), (-4, 3, 3), c="wing"),
    P("footL", "body", (-1.5, 0, -1.5, 3, 8, 3), (2, 12, 0), c="skin2"), P("footR", "body", (-1.5, 0, -1.5, 3, 8, 3), (-2, 12, 0), c="skin2")]
SPECIES["dinolfos"] = _cp2.deepcopy(SPECIES["lizalfos"])
SPECIES["dinolfos"]["parts"] += [P("padL", "body", (0, -2, -3.5, 5, 4, 7), (4, 0, 0), c="horn"), P("padR", "body", (-5, -2, -3.5, 5, 4, 7), (-4, 0, 0), c="horn"), P("crown", "head", (-3.5, -2, -3.5, 7, 2, 7), (0, -6, 0), c="horn")]
SPECIES["kargarok"] = dict(hunch=0.0, parts=[
    P("body", None, (-4, -3, -6, 8, 7, 12), (0, 14, 0), c="skin"), P("head", None, (-3, -3, -3, 6, 6, 6), (0, 13, -7), c="skin2", f=["eyes"]),
    P("beak", "head", (-1.5, -1, -9, 3, 2, 6), (0, 0, 0), c="horn"), P("crest", "head", (-1, -6, -1, 2, 4, 5), (0, 0, 0), c="horn"),
    P("wingL", "body", (0, -0.5, -4, 18, 1, 9), (4, -2, 0), c="wing"), P("wingR", "body", (-18, -0.5, -4, 18, 1, 9), (-4, -2, 0), c="wing"),
    P("tail1", "body", (-2, -1, 0, 4, 2, 7), (0, 0, 6), c="wing"), P("footL", "body", (-1, 3, -1, 2, 5, 2), (2, 0, -1), c="horn"), P("footR", "body", (-1, 3, -1, 2, 5, 2), (-2, 0, -1), c="horn")])

def sp(**k): return pal(**k)
PAL["stalfos"] = ranks5(pal("#dcd8c4", "#b8b49c", "#e8e4d0", "#6a4a3a", "#8a7a60", eye="#ff4020"))
PAL["stalmaster"] = ranks5(pal("#d8b840", "#a88820", "#e8d070", "#5a3a6a", "#fff0a0", eye="#ff4020"))
PAL["dark_lizalfos"] = ranks5(pal("#3a2a4a", "#26183a", "#6a5a7a", "#4a3a5a", "#c040e0", eye="#ff40ff"))
PAL["armos"] = ranks5(pal("#8a8a78", "#6a6a5a", "#a0a090", "#000000", "#48d8e8", eye="#48d8e8"))
PAL["beamos"] = ranks5(pal("#7a7a8a", "#5a5a6a", "#9a9aa8", "#000000", "#ff3030", eye="#ff3030"))
PAL["skulltula"] = ranks5(pal("#4a3a2a", "#2a2018", "#6a5a44", "#000000", "#d8a020", eye="#ff3030"))
PAL["deku_baba"] = ranks5(pal("#c04a3a", "#3a7a2a", "#8a2a2a", "#000000", "#e8d84a", eye="#ffee60"))
PAL["cursed_bokoblin"] = ranks5(pal("#5a2a6a", "#3a1a4a", "#8a5a98", "#2a1a30", "#d02a8a", eye="#ff2a6a"))
PAL["ghirahim"] = ranks5(pal("#f0f0f4", "#d0d0dc", "#ffffff", "#2a2a38", "#8a2ad8", hair="#f4f4f8", eye="#ffcc20"))
PAL["demise"] = ranks5(pal("#4a2a2a", "#2e1a1a", "#7a4a3a", "#2a2028", "#ff5a20", hair="#d83a1a", eye="#ffcc20"))
PAL["moldarach"] = ranks5(pal("#c8a060", "#a07a40", "#d8b878", "#000000", "#e8e0c0", eye="#ff4020"))
PAL["koloktos"] = ranks5(pal("#8a7a50", "#6a5a38", "#a89868", "#000000", "#48d8e8", eye="#48d8e8"))
PAL["scaldera"] = ranks5(pal("#5a3a2a", "#3a2418", "#7a5a3a", "#000000", "#ff6a10", eye="#ffcc20"))
PAL["techno_bokoblin"] = ranks5(pal("#3a8a9a", "#286a78", "#80c8d8", "#2a4a58", "#40ffff", eye="#40ffff"))
PAL["quadro_baba"] = ranks5(pal("#3a8a3a", "#2a6a2a", "#d83a3a", "#000000", "#e8d84a", eye="#ffee60"))
PAL["keese_dark"] = ranks5(pal("#3a2a4a", "#26183a", "#5a4a6a", "#000000", "#a040e0", wing="#4a2a5a", eye="#ff40ff"))
PAL["wall_skulltula"] = ranks5(pal("#5a4a3a", "#3a2a20", "#7a6a54", "#000000", "#d8a020", eye="#ff3030"))
PAL["petit_moldorm"] = ranks5(pal("#c8a878", "#a08858", "#e0c898", "#000000", "#e8e0c0", eye="#ff4020"))
PAL["shakomite"] = ranks5(pal("#c88a50", "#a06a38", "#e8c890", "#000000", "#fff040", eye="#ff4020"))
PAL["frog_magma"] = ranks5(pal("#c84a20", "#a03410", "#ff8a40", "#000000", "#ffcc20", eye="#ffee20"))
PAL["frog_elec"] = ranks5(pal("#c8b830", "#a09020", "#f0e880", "#000000", "#ffff80", eye="#ffff40"))
PAL["frog_dark"] = ranks5(pal("#3a2a4a", "#26183a", "#6a5a7a", "#000000", "#c040e0", eye="#ff40ff"))
PAL["frog_water"] = ranks5(pal("#3a7ac8", "#285a98", "#80b8f0", "#000000", "#a0e0ff", eye="#ffee20"))
PAL["don_gerar"] = ranks5(pal("#6a7a8a", "#4a5a68", "#8a9aa8", "#7a3a2a", "#d8b840", eye="#ff4020"))
PAL["don_killer"] = ranks5(pal("#7a6a8a", "#5a4a68", "#9a8aa8", "#3a3a7a", "#d8b840", eye="#ff4020"))
PAL["gumarm"] = ranks5(pal("#6a2a1a", "#4a1a10", "#8a3a22", "#000000", "#ff7a20", eye="#ffcc20"))
PAL["paraspalas"] = ranks5(pal("#7a5a6a", "#583a4a", "#9a7a8a", "#000000", "#e0a0e0", eye="#ff40a0"))
PAL["bulblin"] = ranks5(pal("#c85a3a", "#9a3a22", "#e8a078", "#4a3a2a", "#d8c8a0", hair="#5a2a1a", eye="#ffee40"))
PAL["king_bulblin"] = ranks5(pal("#b8643a", "#8a4422", "#e0a070", "#3a4a8a", "#e8d070", hair="#2a1a10", eye="#ffee40"))
PAL["stalhound"] = ranks5(pal("#d8d4c0", "#b4b09a", "#e8e4d0", "#000000", "#c8c4b0", eye="#60d8ff"))
PAL["shadow_beast"] = ranks5(pal("#14141c", "#0c0c12", "#2a2a38", "#000000", "#e8e8f0", eye="#ff3a3a"))
PAL["redead"] = ranks5(pal("#8a8a78", "#666656", "#a8a896", "#6a6a58", "#c8c8b0", eye="#ff3030"))
PAL["poe"] = ranks5(pal("#5a6a5a", "#3a4a3a", "#8a9a8a", "#3a2a4a", "#ffb030", eye="#ff4020"))
PAL["tektite"] = ranks5(pal("#c85a30", "#9a4020", "#e8a070", "#000000", "#ffd030", eye="#ffee40"))
PAL["peahat"] = ranks5(pal("#6a9a3a", "#4a7a28", "#d8d86a", "#000000", "#e8a030", eye="#ff4020"))
PAL["bubble_fire"] = ranks5(pal("#e8e0c8", "#c8c0a8", "#f8f0d8", "#000000", "#ff7a20", eye="#ffcc20"))
PAL["bubble_ice"] = [dict(q, horn="#80d8ff", eye="#c0f0ff") for q in PAL["bubble_fire"]]
PAL["bubble_dark"] = [dict(q, horn="#a040e0", eye="#ff40ff", skin="#4a3a5a", skin2="#2a1a3a") for q in PAL["bubble_fire"]]
PAL["dodongo"] = ranks5(pal("#8a6a3a", "#6a4a24", "#d8b878", "#000000", "#e8e0c0", eye="#ffcc20"))
PAL["helmasaur"] = ranks5(pal("#5a6a5a", "#3a4a3a", "#8a9a8a", "#000000", "#8a7a5a", eye="#ffcc20"))
PAL["dark_nut"] = ranks5(pal("#2a2a34", "#1a1a22", "#4a4a58", "#5a1a1a", "#c83a3a", eye="#ff3a3a"))
PAL["death_sword"] = ranks5(pal("#d0ccd8", "#a8a4b8", "#e0dce8", "#4a2a6a", "#8a60c8", eye="#c0a0ff"))
PAL["zant"] = ranks5(pal("#d8d4e0", "#2a2a3a", "#3a3a4a", "#1a1a28", "#d8c040", eye="#ffcc20"))
PAL["ganondorf"] = ranks5(pal("#8a5a3a", "#5a3a28", "#a8785a", "#1a1a22", "#d8a020", hair="#c83a1a", eye="#ffcc20"))
PAL["diababa"] = ranks5(pal("#3a7a3a", "#285a28", "#a8d878", "#000000", "#e8e060", eye="#ff4020"))
PAL["argorok"] = ranks5(pal("#a83a2a", "#7a2418", "#e0c890", "#000000", "#e8dcb8", wing="#c84a30", eye="#ffee55"))
PAL["fyrus"] = ranks5(pal("#8a3a20", "#5a2210", "#c06a40", "#000000", "#ff7a20", hair="#e8d8b0", eye="#ffcc20"))
PAL["armogohma"] = ranks5(pal("#4a4a58", "#2e2e3a", "#7a7a88", "#000000", "#c8d8ff", eye="#ff4040"))
PAL["aeralfos"] = ranks5(pal("#9a5a3a", "#7a4228", "#e0c890", "#6a4a3a", "#e8dcb8", wing="#7a3a28", eye="#ffd030"))
PAL["dinolfos"] = ranks5(pal("#8a3a2a", "#6a2a1e", "#d8b878", "#4a3a2a", "#d8c070", eye="#ffd030"))
PAL["kargarok"] = ranks5(pal("#6a4a3a", "#4a3224", "#d8b888", "#000000", "#e8a830", wing="#7a5a40", eye="#ffcc20"))
for _k in ("bulblin", "king_bulblin", "stalhound", "shadow_beast", "redead", "poe", "tektite", "peahat", "bubble_fire", "bubble_ice", "bubble_dark", "dodongo", "helmasaur", "dark_nut", "death_sword", "zant", "ganondorf", "diababa", "argorok", "fyrus", "armogohma", "aeralfos", "dinolfos", "kargarok"):
    for _p in PAL[_k]: _p.setdefault("nose", "#e8a0a8"); _p.setdefault("bandage", "#ece8d8"); _p.setdefault("bone", _p["skin2"]); _p.setdefault("joint", _p["horn"])
PAL["tentalus"] = ranks5(pal("#4a7a8a", "#345a68", "#8ab8c8", "#000000", "#e8e0a0", eye="#ff4a30"))
PAL["the_imprisoned"] = ranks5(pal("#6a5a78", "#4a3a58", "#8a7a98", "#000000", "#e8e0d0", eye="#ff4a20"))
for _k in ("stalfos", "stalmaster", "dark_lizalfos", "armos", "beamos", "skulltula", "deku_baba", "cursed_bokoblin", "ghirahim", "demise", "moldarach", "koloktos", "scaldera", "the_imprisoned", "tentalus", "techno_bokoblin", "quadro_baba", "keese_dark", "wall_skulltula", "petit_moldorm", "shakomite", "frog_magma", "frog_elec", "frog_dark", "frog_water", "don_gerar", "don_killer", "gumarm", "paraspalas"):
    for _p in PAL[_k]: _p.setdefault("nose", "#c4bca4"); _p.setdefault("bandage", "#ece8d8"); _p.setdefault("bone", _p["skin2"]); _p.setdefault("joint", _p["horn"])

TEX = 128


def pack(parts):
    """shelf-pack box nets into TEXxTEX; returns uv per part (mutates)."""
    items = []
    for p in parts:
        w, h, d = p["box"][3:6]
        w, h, d = int(round(w)), int(round(h)), int(round(d))
        items.append((p, 2 * (w + d), h + d))
    items.sort(key=lambda x: -x[2])
    x = y = rowh = 0
    for p, W, H in items:
        if x + W > TEX:
            x, y, rowh = 0, y + rowh, 0
        p["uv"] = [x, y]
        x += W
        rowh = max(rowh, H)
    assert y + rowh <= TEX, "texture overflow"


def paint_box(img, p, col, rng, palette):
    u, v = p["uv"]
    w, h, d = [int(round(t)) for t in p["box"][3:6]]
    faces = {"top": (u + d, v, w, d, 1.15), "bottom": (u + d + w, v, w, d, 0.7),
             "right": (u, v + d, d, h, 0.9), "front": (u + d, v + d, w, h, 1.0),
             "left": (u + d + w, v + d, d, h, 0.85), "back": (u + 2 * d + w, v + d, w, h, 0.8)}
    px = img.load()
    for name, (fx, fy, fw, fh, s) in faces.items():
        for i in range(fw):
            for j in range(fh):
                n = rng.uniform(0.9, 1.08)
                grad = 1.04 - 0.1 * (j / max(1, fh))  # darker toward bottom
                px[fx + i, fy + j] = shade(col, s * n * grad) + (255,)
        if "stripes" in p["f"]:
            for j in range(0, fh, 3):
                for i in range(fw): px[fx + i, fy + j] = shade(col, 0.72) + (255,)
        if "circuit" in p["f"]:
            glow = hexc(palette["horn"]) + (255,)
            for j in range(2, fh, 4):
                for i in range(fw):
                    if (i + j) % 7 < 4: px[fx + i, fy + j] = glow
            for i in range(3, fw, 6):
                for j in range(fh):
                    if j % 5 < 3: px[fx + i, fy + j] = shade(hexc(palette["horn"]), 0.8) + (255,)
        if name == "front":
            feat = p["f"]
            if "belly" == p["c"] and fw > 2:
                pass
            if "eyes" in feat and fw >= 6:
                ey = fy + max(2, fh // 3)
                for ex in (fx + 1, fx + fw - 3):
                    px[ex, ey] = (255, 255, 255, 255); px[ex + 1, ey] = hexc(palette["eye"]) + (255,)
                    px[ex, ey + 1] = (20, 10, 10, 255); px[ex + 1, ey + 1] = (20, 10, 10, 255)
                for ex in (fx, fx + 1, fx + fw - 3, fx + fw - 2):  # angry brow
                    px[ex, ey - 1] = shade(col, 0.45) + (255,)
            if "eyes" in feat and fw >= 7 and fh >= 7: # mouth line with teeth
                my = fy + fh - 2
                for mx in range(fx + 2, fx + fw - 2):
                    px[mx, my] = shade(col, 0.35) + (255,)
                    if (mx - fx) % 2 == 0: px[mx, my - 1] = (236, 232, 218, 255)
            if "bigeye" in feat:
                cx, cy = fx + fw // 2, fy + fh // 2
                for i in range(-2, 2):
                    for j in range(-2, 2):
                        px[cx + i, cy + j] = (240, 240, 240, 255)
                for i in (-1, 0):
                    for j in (-1, 0):
                        px[cx + i, cy + j] = hexc(palette["eye"]) + (255,)
                px[cx - 1, cy - 1] = (10, 0, 0, 255)
            if "nostrils" in feat:
                px[fx + 1, fy + fh - 2] = shade(col, 0.4) + (255,)
                px[fx + fw - 2, fy + fh - 2] = shade(col, 0.4) + (255,)
        if "eyes_side" in p["f"] and name in ("right", "left"):
            px[fx + fw // 2, fy + fh // 3] = hexc(palette["eye"]) + (255,)
        if "hand" in p["f"] and name != "top":
            for i in range(fw):
                for j in range(max(0, fh - 3), fh):
                    px[fx + i, fy + j] = shade(hexc(palette["skin2"]), s) + (255,)


def order_parts(parts):
    done, out = set(), []
    while len(out) < len(parts):
        for q in parts:
            if q["n"] not in done and (q["p"] is None or q["p"] in done): out.append(q); done.add(q["n"])
    return out


STYLE = {}
for _s in ("bokoblin", "moblin", "lynel", "hinox", "horriblin", "techno_bokoblin", "cursed_bokoblin", "bulblin", "king_bulblin", "keese", "keese_fire", "keese_ice", "keese_elec",
           "keese_dark", "kargarok", "gibdo", "redead", "stalhound", "shadow_beast", "demise", "ganondorf", "quadro_baba", "deku_baba", "skulltula", "wall_skulltula", "tektite"): STYLE[_s] = "fur"
for _s in ("lizalfos", "lizalfos_fire", "lizalfos_ice", "lizalfos_elec", "dark_lizalfos", "dinolfos", "aeralfos", "dodongo", "helmasaur", "gleeok", "argorok", "diababa", "octorok", "shakomite", "moldarach"): STYLE[_s] = "scale"
for _s in ("stalkoblin", "stalmoblin", "stalizalfos", "stalhinox", "stalfos", "stalmaster", "death_sword"): STYLE[_s] = "bone"
for _s in ("guardian", "decayed_guardian", "guardian_turret", "guardian_skywatcher", "calamity_ganon", "guardian_scout_1", "guardian_scout_2", "guardian_scout_3", "guardian_scout_4",
           "beamos", "armos", "soldier_construct", "captain_construct", "koloktos", "dark_nut", "don_gerar", "don_killer", "fyrus", "armogohma", "paraspalas"): STYLE[_s] = "metal"
for _s in ("talus", "frox", "scaldera", "gumarm", "the_imprisoned", "tentalus"): STYLE[_s] = "stone"
for _s in ("wizzrobe", "blizzrobe", "thunder_wizzrobe", "ghirahim", "zant", "poe", "yiga_footsoldier", "yiga_blademaster", "master_kohga", "phantom_ganon",
           "fireblight_ganon", "waterblight_ganon", "windblight_ganon", "thunderblight_ganon"): STYLE[_s] = "cloth"
ALPHA = {"chuchu": 175, "poe": 205, "bubble_fire": 225, "bubble_ice": 225, "bubble_dark": 225}
GLOW_HORN = set("guardian decayed_guardian guardian_turret guardian_skywatcher calamity_ganon guardian_scout_1 guardian_scout_2 guardian_scout_3 guardian_scout_4 beamos armos koloktos "
                "scaldera gumarm talus frox demise bubble_fire bubble_ice bubble_dark poe fireblight_ganon waterblight_ganon windblight_ganon thunderblight_ganon fyrus ghirahim "
                "chuchu soldier_construct captain_construct shadow_beast cursed_bokoblin techno_bokoblin zant armogohma".split())
RANK_EXTRA = set("bokoblin moblin lizalfos stalkoblin stalmoblin stalizalfos gibdo yiga_footsoldier yiga_blademaster soldier_construct armos bulblin dark_lizalfos techno_bokoblin "
                 "cursed_bokoblin dark_nut stalfos horriblin lynel hinox".split())


def rank_extras(parts):
    """silver/black/gold variants get plates, helmet band and crown spikes."""
    byn = {q["n"]: q for q in parts}
    out = []
    head, ra, la = byn.get("head"), byn.get("rightArm"), byn.get("leftArm")
    for arm, nm in ((ra, "plateR"), (la, "plateL")):
        if arm:
            x, y, z, w, h, d = arm["box"]
            out.append(P(nm, arm["n"], (x - 0.8, y - 1.5, z - 0.8, w + 1.6, 3, d + 1.6), (0, 0, 0), c="horn", r=2))
    if head:
        x, y, z, w, h, d = head["box"]
        out.append(P("band", "head", (x - 0.6, y + h * 0.28, z - 0.6, w + 1.2, 1.6, d + 1.2), (0, 0, 0), c="horn", r=3))
        for k, dx in enumerate((-0.28, 0.0, 0.28)):
            out.append(P(f"crown{k}", "head", (x + w / 2 + dx * w - 0.75, y - 3.2, z + d / 2 - 0.75, 1.5, 3.4, 1.5), (0, 0, 0), c="horn", r=4))
    return out


DETAIL = set("bokoblin moblin lizalfos lizalfos_fire lizalfos_ice lizalfos_elec dark_lizalfos dinolfos hinox lynel gibdo redead horriblin cursed_bokoblin techno_bokoblin bulblin king_bulblin "
             "stalkoblin stalmoblin stalizalfos stalhinox stalfos stalmaster frox talus yiga_footsoldier phantom_ganon fireblight_ganon waterblight_ganon windblight_ganon thunderblight_ganon "
             "ganondorf demise zant ghirahim armos dark_nut soldier_construct captain_construct fyrus".split())


def detail_extras(parts):
    """claws on hands, toes on feet, knuckle/forearm bracers, lower tusks: small parts that break up the silhouette."""
    byn = {q["n"]: q for q in parts}; out = []
    for nm in ("rightArm", "leftArm"):
        a = byn.get(nm)
        if not a: continue
        x, y, z, w, h, d = a["box"]
        for k in range(3):  # three claws
            cx = x + w * (0.2 + 0.3 * k) - 0.4
            out.append(P(f"claw{nm[0]}{k}", nm, (cx, y + h - 0.2, z - 0.6, 0.8, 2.2, 0.8), (0, 0, 0), c="horn"))
        out.append(P(f"bracer{nm[0]}", nm, (x - 0.5, y + h * 0.55, z - 0.5, w + 1, 2.2, d + 1), (0, 0, 0), c="cloth", f=["stripes"]))
    for nm in ("rightLeg", "leftLeg"):
        l = byn.get(nm)
        if not l: continue
        x, y, z, w, h, d = l["box"]
        for k in range(3):  # toes
            out.append(P(f"toe{nm[0]}{k}", nm, (x + w * (0.1 + 0.3 * k), y + h - 1.4, z - 1.6, max(0.8, w * 0.25), 1.4, 1.7), (0, 0, 0), c="horn"))
    sn = byn.get("snout")
    if sn:
        x, y, z, w, h, d = sn["box"]
        out.append(P("lowerTuskL", sn["p"], (x + w - 1.2, y + h - 0.2, z + 0.5, 0.9, 2.4, 0.9), (0, 0, 0), c="bandage"))
        out.append(P("lowerTuskR", sn["p"], (x + 0.3, y + h - 0.2, z + 0.5, 0.9, 2.4, 0.9), (0, 0, 0), c="bandage"))
    return out


def refine_geometry(parts):
    """break up the box silhouette: elbows/knees, shoulder caps, brow ridge, cheeks, chin, chest ridge, spine bumps."""
    byn = {q["n"]: q for q in parts}; out = []
    for nm in ("rightArm", "leftArm", "rightLeg", "leftLeg"):
        a = byn.get(nm)
        if not a or a["box"][4] < 8: continue
        x, y, z, w, h, d = a["box"]
        out.append(P(f"joint{nm[0]}{nm[-3]}", nm, (x - 0.7, y + h * 0.42, z - 0.7, w + 1.4, 3, d + 1.4), (0, 0, 0), c=a["c"]))
        if "Arm" in nm: out.append(P(f"cap{nm[0]}", nm, (x - 0.9, y - 1.8, z - 0.9, w + 1.8, 3.6, d + 1.8), (0, 0, 0), c=a["c"]))
    hd = byn.get("head")
    if hd and hd["box"][3] >= 6:
        x, y, z, w, h, d = hd["box"]
        out.append(P("browRidge", "head", (x - 0.4, y + h * 0.18, z - 0.9, w + 0.8, 1.6, 1.8), (0, 0, 0), c="skin2"))
        out.append(P("cheekL", "head", (x + w - 0.8, y + h * 0.45, z + d * 0.15, 1.6, h * 0.3, d * 0.45), (0, 0, 0), c=hd["c"]))
        out.append(P("cheekR", "head", (x - 0.8, y + h * 0.45, z + d * 0.15, 1.6, h * 0.3, d * 0.45), (0, 0, 0), c=hd["c"]))
        out.append(P("chin", "head", (x + w * 0.25, y + h - 1.2, z - 0.6, w * 0.5, 2, 1.6), (0, 0, 0), c="skin2"))
    bd = byn.get("body")
    if bd and bd["box"][3] >= 6:
        x, y, z, w, h, d = bd["box"]
        out.append(P("chestRidge", "body", (x + w * 0.1, y + 1, z - 0.8, w * 0.8, h * 0.4, 1.6), (0, 0, 0), c="skin2"))
        for k in range(3): out.append(P(f"spineBump{k}", "body", (x + w / 2 - 0.8, y + h * (0.12 + 0.25 * k), z + d - 0.3, 1.6, 1.8, 1.4), (0, 0, 0), c="horn"))
    return out


ROUND = {"chuchu": ["body"], "octorok": ["body"], "keese": ["body"], "keese_fire": ["body"], "keese_ice": ["body"], "keese_elec": ["body"], "keese_dark": ["body"],
         "peahat": ["body"], "bubble_fire": ["body"], "bubble_ice": ["body"], "bubble_dark": ["body"], "tentalus": ["body"], "scaldera": ["body"], "paraspalas": ["body"],
         "guardian_skywatcher": ["body"], "bulblin": ["belly"], "moblin": ["belly"], "bokoblin": ["belly"], "hinox": ["belly"], "horriblin": [], "poe": ["head"], "shakomite": ["shell"]}


def roundify(parts, names):
    """approximate an ellipsoid with 4 stacked slabs (narrow-wide-wide-narrow); features stay on the widest front slab."""
    out = []
    for q in parts:
        if q["n"] not in names or q["box"][4] < 4: out.append(q); continue
        x, y, z, w, h, d = q["box"]; sl = h / 4; fac = (0.62, 1.0, 1.0, 0.62)
        for k in range(4):
            nw, nd = w * fac[k], d * fac[k]
            nq = dict(q); nq["n"] = q["n"] if k == 1 else f'{q["n"]}_s{k}'
            if k != 1: nq["p"] = q["n"]; nq["pose"] = [0, 0, 0]; nq["rot"] = [0, 0, 0]
            nq["box"] = [x + (w - nw) / 2, y + sl * k, z + (d - nd) / 2, nw, sl, nd]; nq["f"] = q["f"] if k == 1 else []; nq["r"] = q.get("r", 0)
            out.append(nq)
        for c in out[-4:]:
            pass
    # re-parent children of the original part: they keep pointing at q["n"] which is slab 1 (same name)
    return out


def split_limbs(parts, names=("rightArm", "leftArm", "rightLeg", "leftLeg")):
    """elbow/knee joints: upper + lower segment (children below the joint follow the lower segment)."""
    out = [dict(q) for q in parts]; byn = {q["n"]: q for q in out}; new = []
    for nm in names:
        a = byn.get(nm)
        if not a or a["box"][4] < (5 if "Leg" in nm and "front" in nm or "back" in nm else 8): continue
        x, y, z, w, h, d = a["box"]; cut = y + h * 0.5; lo = nm + "Low"
        a["box"] = [x, y, z, w, cut - y, d]
        new.append(P(lo, nm, (x, 0, z, w, y + h - cut, d), (0, cut, 0), c=a["c"], f=[f for f in a["f"] if f == "hand"]))
        a["f"] = [f for f in a["f"] if f != "hand"]
        for q in out:
            if q["p"] == nm and (q["box"][1] + q["box"][4] / 2) >= cut:
                q["p"] = lo; q["box"][1] -= cut
    return order_parts(out + new)


def style_pass(img, glowmask, p, sid, rng, palette):
    st = STYLE.get(sid, "skin")
    u, v = p["uv"]
    w, h, d = [int(round(t)) for t in p["box"][3:6]]
    faces = [(u + d, v, w, d), (u + d + w, v, w, d), (u, v + d, d, h), (u + d, v + d, w, h), (u + d + w, v + d, d, h), (u + 2 * d + w, v + d, w, h)]
    px = img.load(); gm = glowmask.load()
    def mul(x, y, f):
        if gm[x, y][3]: return
        r, g, b, a = px[x, y]; px[x, y] = (min(255, int(r * f)), min(255, int(g * f)), min(255, int(b * f)), a)
    for (fx, fy, fw, fh) in faces:
        for i in range(fw):
            for j in range(fh):
                if st == "fur":
                    if (i * 7 + 3) % 5 == 0 and rng.random() < 0.6: mul(fx + i, fy + j, 0.88)
                    elif rng.random() < 0.05: mul(fx + i, fy + j, 1.14)
                elif st == "scale":
                    if (i + (j % 2) * 2) % 4 == 0 and j % 2 == 0: mul(fx + i, fy + j, 1.16)
                    elif (i + (j % 2) * 2) % 4 == 3: mul(fx + i, fy + j, 0.88)
                elif st == "bone":
                    if rng.random() < 0.06: mul(fx + i, fy + j, 0.78)
                    if (i * 3 + j * 5) % 11 == 0: mul(fx + i, fy + j, 0.85)
                elif st == "metal":
                    if i % 8 == 0 or j % 8 == 0: mul(fx + i, fy + j, 0.8)
                    elif i % 8 == 1 and j % 8 == 1: mul(fx + i, fy + j, 1.25)
                    elif rng.random() < 0.03: mul(fx + i, fy + j, 1.3)
                elif st == "stone":
                    if ((i // 3) * 5 + (j // 3) * 3) % 4 == 0: mul(fx + i, fy + j, 0.9)
                    if rng.random() < 0.05: mul(fx + i, fy + j, 0.7)
                elif st == "cloth":
                    mul(fx + i, fy + j, 0.96 if (i + j) % 2 else 1.04)
                if i in (0, fw - 1) or j in (0, fh - 1): mul(fx + i, fy + j, 0.86)  # edge shading


def glow_pass(img, glowmask, p, sid, palette):
    """copy glowing pixels (eyes, circuit lines, glowing parts) into the emissive mask."""
    u, v = p["uv"]
    w, h, d = [int(round(t)) for t in p["box"][3:6]]
    eye, horn = hexc(palette["eye"]) + (255,), hexc(palette["horn"]) + (255,)
    px = img.load(); gm = glowmask.load()
    for (fx, fy, fw, fh) in [(u + d, v, w, d), (u + d + w, v, w, d), (u, v + d, d, h), (u + d, v + d, w, h), (u + d + w, v + d, d, h), (u + 2 * d + w, v + d, w, h)]:
        for i in range(fw):
            for j in range(fh):
                c = px[fx + i, fy + j]
                if c == eye or (c == horn and ("circuit" in p["f"] or (p["c"] == "horn" and sid in GLOW_HORN))) or (p["c"] == "horn" and sid in GLOW_HORN and c[3]):
                    gm[fx + i, fy + j] = c


def gen_damage():
    rng = random.Random(7); im = Image.new("RGBA", (TEX, TEX), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for _ in range(46):  # cracks / scratches
        x, y = rng.randrange(TEX), rng.randrange(TEX)
        for _ in range(rng.randrange(3, 9)):
            nx, ny = x + rng.choice((-1, 0, 1)) * rng.randrange(1, 3), y + rng.choice((0, 1)) * rng.randrange(1, 3)
            d.line([(x, y), (nx, ny)], fill=(25, 10, 10, 200)); x, y = nx, ny
    for _ in range(30):  # blood / scorch blotches
        x, y = rng.randrange(TEX), rng.randrange(TEX); r = rng.randrange(1, 3)
        d.ellipse([x, y, x + r, y + r], fill=(110, 12, 12, 170))
    im.save(f"{A}/textures/entity/damage.png")


def _sh(c, f): return tuple(max(0, min(255, int(v * f))) for v in c[:3])


def special(sid, p, fname, dr, gd, fw, fh, palette, rng):
    """bespoke decals for the flagship creatures."""
    n = p["n"]; col = hexc(palette[p["c"]]); dk = _sh(col, 0.45) + (230,); lt = _sh(col, 1.4) + (220,)
    if sid in ("bokoblin", "horriblin", "techno_bokoblin", "cursed_bokoblin", "stalkoblin"):
        if n == "belly" and fname == "front":
            dr.ellipse([fw // 2 - 3, fh // 2, fw // 2 + 3, fh // 2 + 5], fill=dk)  # navel
            for k in range(5): dr.point((fw // 2 + rng.randrange(-8, 9), fh // 2 + rng.randrange(-8, 9)), fill=dk)
        if n in ("wrapR", "wrapL"):
            for k in range(0, fh, 5): dr.line([(0, k), (fw, k + 3)], fill=(150, 140, 120, 200), width=1)  # diagonal binding
            dr.rectangle([fw // 2 - 2, 2, fw // 2 + 2, 6], fill=(120, 110, 95, 255))  # knot
        if n in ("earL", "earR") and fname in ("front", "back"):
            dr.ellipse([fw * 0.2, fh * 0.2, fw * 0.8, fh * 0.8], fill=_sh(col, 1.25) + (200,))
        if n == "head" and fname == "front":
            for k in (-1, 1): dr.line([(fw // 2 + k * 3, 3), (fw // 2 + k * 6, 8)], fill=dk)  # forehead wrinkles
        if n == "horn":
            for k in range(3, fh, 5): dr.line([(0, k), (fw, k - 1)], fill=dk)  # horn ridges
    elif sid in ("moblin", "stalmoblin"):
        if n in ("wrapR", "wrapL"):
            for k in range(0, fw, 4): dr.line([(k, 0), (fw - k, fh)], fill=(150, 140, 120, 190)); dr.line([(fw - k, 0), (k, fh)], fill=(150, 140, 120, 190))  # cross binding
        if n == "body" and fname == "front":
            dr.line([(fw // 4, 4), (fw * 3 // 4, fh // 2)], fill=lt, width=1); dr.line([(fw // 4 + 1, 4), (fw * 3 // 4 + 1, fh // 2)], fill=dk)  # scar
        if n == "snout" and fname == "front":
            for k in range(3): dr.arc([2, 2 + k * 3, fw - 2, 6 + k * 3], 200, 340, fill=dk)  # snout wrinkles
    elif sid in ("lizalfos", "dark_lizalfos", "lizalfos_fire", "lizalfos_ice", "lizalfos_elec", "stalizalfos"):
        if n == "vest":
            for _ in range(fw * fh // 40):
                x, y = rng.randrange(fw), rng.randrange(fh); dr.ellipse([x, y, x + 3, y + 2], outline=dk)  # leopard rosettes
        if n == "belly" and fname == "front":
            for k in range(2, fh, 4): dr.line([(0, k), (fw, k)], fill=dk)  # belly plates
        if n in ("head", "snout") and fname == "top":
            for k in range(0, fw, 4): dr.line([(k, 0), (k + 1, fh)], fill=dk)  # head ridges
    elif sid in ("lynel", "shadow_beast"):
        if n in ("belly", "body") and fname == "front":
            for k in range(0, fh, 6):
                dr.rectangle([1, k, fw - 2, k + 4], outline=dk); dr.point((3, k + 2), fill=lt); dr.point((fw - 4, k + 2), fill=lt)  # armor plates
        if n == "mane":
            for k in range(0, fw, 2): dr.line([(k, 0), (k + rng.randrange(-1, 2), fh)], fill=(_sh(col, rng.choice((0.7, 1.3))) + (170,)))  # strands
    elif sid in ("hinox", "stalhinox"):
        if n == "brow":
            for k in range(0, fw, 2): dr.line([(k, fh), (k + rng.randrange(-2, 3), 0)], fill=_sh(col, rng.choice((0.8, 1.1))) + (230,))  # bushy brow
        if n == "vest" and fname in ("front", "back"):
            dr.line([(0, fh - 3), (fw, fh - 3)], fill=(150, 125, 80, 255), width=2)
            for k in range(3, fw, 8): dr.ellipse([k, fh - 5, k + 3, fh - 2], fill=(110, 90, 55, 255))  # rope knots
        if n == "belly" and fname == "front":
            for _ in range(fw * fh // 30): x, y = rng.randrange(fw), rng.randrange(fh); dr.line([(x, y), (x + 1, y + 2)], fill=dk)  # sparse hair
    elif sid in ("talus", "frox", "stalhinox"):
        if sid != "stalhinox" and n in ("body", "rock1", "rightArm", "leftArm"):
            for _ in range(fw * fh // 60):  # lichen + quartz flecks
                x, y = rng.randrange(fw), rng.randrange(fh); dr.ellipse([x, y, x + 2, y + 1], fill=(210, 205, 190, 200) if rng.random() < 0.5 else (95, 130, 70, 160))
    elif sid in ("gibdo", "redead", "stalfos", "stalmaster", "death_sword"):
        if n in ("body", "ribs") and fname == "front":
            for k in range(2, fh - 2, 4): dr.arc([1, k, fw - 1, k + 6], 0, 180, fill=dk)  # rib arcs
        if n == "head" and fname == "front":
            dr.polygon([(fw // 2, fh // 2 + 1), (fw // 2 - 2, fh // 2 + 5), (fw // 2 + 2, fh // 2 + 5)], fill=dk)  # nose cavity
        if sid in ("gibdo", "redead") and n in ("wrap", "wrap2", "body"):
            for k in range(0, fh, 4): dr.line([(0, k), (fw, k + 2)], fill=(120, 110, 90, 220))  # mummy wraps
    elif sid in ("wizzrobe", "blizzrobe", "thunder_wizzrobe", "zant", "ghirahim"):
        if n in ("body", "hem", "robe") and fname in ("front", "back"):
            dr.line([(fw // 2, 0), (fw // 2, fh)], fill=hexc(palette["hair"]) + (230,), width=2)  # center trim
            for k in range(2, fh, 6): dr.line([(fw // 2 - 3, k), (fw // 2 + 3, k)], fill=lt)
        if n in ("cone", "hood", "helm") and fname == "front":
            dr.arc([2, fh // 3, fw - 2, fh + fh // 3], 180, 360, fill=dk)
    elif sid in ("keese", "keese_fire", "keese_ice", "keese_elec", "keese_dark", "kargarok"):
        if n.startswith("wing"):
            for k in range(2, fw, 5): dr.line([(k, 0), (k + 3, fh)], fill=dk)  # wing veins
            dr.rectangle([0, 0, fw - 1, 1], fill=lt)
    elif sid in ("chuchu",):
        if n == "body":
            for _ in range(fw * fh // 40): x, y = rng.randrange(fw), rng.randrange(fh); dr.ellipse([x, y, x + 2, y + 2], fill=(255, 255, 255, 90))  # bubbles
    elif sid in ("fireblight_ganon", "waterblight_ganon", "windblight_ganon", "thunderblight_ganon", "calamity_ganon", "ganondorf", "demise", "phantom_ganon"):
        if n in ("body", "robe", "cape") and fname in ("front", "back"):
            for k in range(3, fw - 3, 5):  # glowing vein cracks
                y = rng.randrange(fh // 2); pts = [(k, y)]
                for _ in range(4): pts.append((pts[-1][0] + rng.randrange(-2, 3), pts[-1][1] + rng.randrange(2, 5)))
                dr.line(pts, fill=hexc(palette["horn"]) + (220,)); gd.line(pts, fill=hexc(palette["horn"]) + (220,))
    elif sid in ("soldier_construct", "captain_construct", "armos", "koloktos", "dark_nut", "fyrus"):
        if n in ("body", "chest", "core"):
            dr.rectangle([fw // 2 - 3, fh // 2 - 3, fw // 2 + 3, fh // 2 + 3], outline=hexc(palette["horn"]) + (255,)); gd.rectangle([fw // 2 - 3, fh // 2 - 3, fw // 2 + 3, fh // 2 + 3], outline=hexc(palette["horn"]) + (255,))
            dr.line([(fw // 2, 0), (fw // 2, fh)], fill=dk)  # chest seam
    elif sid == "chuchu" and n in ("eyeL", "eyeR") and fname == "front":
        cx, cy = fw // 2, fh // 2; r_ = min(fw, fh) // 2 - 1
        dr.ellipse([cx - r_, cy - r_, cx + r_, cy + r_], fill=(250, 250, 245, 255), outline=(230, 120, 30, 255), width=3)
        dr.ellipse([cx - r_ // 2, cy - r_ // 2, cx + r_ // 2, cy + r_ // 2], fill=(235, 130, 20, 255)); dr.ellipse([cx - r_ // 3, cy - r_ // 3, cx + r_ // 3, cy + r_ // 3], fill=(20, 12, 10, 255))
        dr.point((cx - 2, cy - 2), fill=(255, 255, 255, 255))
    elif sid in ("octorok", "tentalus", "peahat", "deku_baba", "quadro_baba", "skulltula", "wall_skulltula", "tektite"):
        if n == "body" and fname in ("top", "front"):
            for _ in range(fw * fh // 50): x, y = rng.randrange(fw), rng.randrange(fh); dr.ellipse([x, y, x + 3, y + 3], outline=dk)  # warts / spots
    elif sid in ("guardian", "decayed_guardian", "guardian_turret", "guardian_skywatcher"):
        if n == "eyeCyl" and fname == "front":
            cx, cy = fw // 2, fh // 2
            for r_ in range(min(fw, fh) // 2, 1, -2): dr.ellipse([cx - r_, cy - r_, cx + r_, cy + r_], outline=_sh(hexc(palette["eye"]), 0.4 + r_ / 14) + (255,)); gd.ellipse([cx - r_, cy - r_, cx + r_, cy + r_], outline=hexc(palette["eye"]) + (200,))
        if n in ("body", "shell2", "dome", "head") and fname in ("top", "front"):
            for k in range(2, fw - 4, 7):  # runic glyphs
                y = fh // 2 + rng.randrange(-3, 4); dr.rectangle([k, y, k + 2, y + 3], outline=hexc(palette["horn"]) + (220,)); gd.rectangle([k, y, k + 2, y + 3], outline=hexc(palette["horn"]) + (220,))


def paint2x(img, glow, parts, sid, palette, seed):
    """hand-painted style details at 2x: shading, ambient occlusion, material strokes, painted faces."""
    rng = random.Random(seed); st = STYLE.get(sid, "skin")
    gpx = glow.load()
    saved = [(x, y, gpx[x, y]) for x in range(img.width) for y in range(img.height) if gpx[x, y][3]]
    for p in parts:
        col = hexc(palette[p["c"]]); u, v = p["uv"]; w, h, d = [int(round(t)) * 1 for t in p["box"][3:6]]
        faces = {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "right": (u, v + d, d, h), "front": (u + d, v + d, w, h), "left": (u + d + w, v + d, d, h), "back": (u + 2 * d + w, v + d, w, h)}
        for fname, (fx, fy, fw, fh) in faces.items():
            fx, fy, fw, fh = fx * 2, fy * 2, fw * 2, fh * 2
            if fw < 4 or fh < 4: continue
            tile = Image.new("RGBA", (fw, fh), (0, 0, 0, 0)); dr = ImageDraw.Draw(tile)
            # light from top-left: soft gradient + ambient occlusion on borders
            for k in range(min(4, fh // 2)):
                dr.line([(0, fh - 1 - k), (fw, fh - 1 - k)], fill=(0, 0, 0, 55 - k * 12))
                dr.line([(0, k), (fw, k)], fill=(255, 255, 255, 26 - k * 6))
            for k in range(min(3, fw // 2)):
                dr.line([(k, 0), (k, fh)], fill=(255, 255, 255, 18 - k * 5)); dr.line([(fw - 1 - k, 0), (fw - 1 - k, fh)], fill=(0, 0, 0, 50 - k * 14))
            area = fw * fh
            if st == "fur":
                for _ in range(area // 14):
                    x, y = rng.randrange(fw), rng.randrange(fh); l = rng.randrange(3, 8); dx = rng.choice((-1, 0, 0, 1))
                    c = _sh(col, rng.choice((0.78, 0.86, 1.18, 1.26))); dr.line([(x, y), (x + dx * l // 2, y + l)], fill=c + (rng.randrange(60, 120),))
            elif st == "scale":
                s_ = 6
                for gy in range(0, fh, s_):
                    for gx in range(-(s_ // 2) * ((gy // s_) % 2), fw, s_):
                        dr.arc([gx, gy, gx + s_, gy + s_ + 2], 0, 180, fill=_sh(col, 0.62) + (150,)); dr.point((gx + 1, gy + 1), fill=_sh(col, 1.35) + (170,))
            elif st == "bone":
                for _ in range(max(2, area // 400)):
                    x, y = rng.randrange(fw), rng.randrange(fh)
                    for _ in range(rng.randrange(3, 8)):
                        nx, ny = x + rng.choice((-2, -1, 1, 2)), y + rng.randrange(1, 4); dr.line([(x, y), (nx, ny)], fill=_sh(col, 0.55) + (170,)); x, y = nx, ny
                for _ in range(area // 120): dr.point((rng.randrange(fw), rng.randrange(fh)), fill=_sh(col, 0.7) + (120,))
            elif st == "metal":
                for _ in range(max(1, area // 500)):
                    if rng.random() < 0.5:
                        y = rng.randrange(fh); dr.line([(0, y), (fw, y)], fill=_sh(col, 0.55) + (150,)); dr.line([(0, y + 1), (fw, y + 1)], fill=_sh(col, 1.3) + (80,))
                    else:
                        x = rng.randrange(fw); dr.line([(x, 0), (x, fh)], fill=_sh(col, 0.55) + (150,)); dr.line([(x + 1, 0), (x + 1, fh)], fill=_sh(col, 1.3) + (80,))
                for gx in range(3, fw - 2, 10):
                    for gy in range(3, fh - 2, 10):
                        if rng.random() < 0.5: dr.ellipse([gx, gy, gx + 2, gy + 2], fill=_sh(col, 1.3) + (170,), outline=_sh(col, 0.5) + (170,))
                for _ in range(area // 250):
                    x, y = rng.randrange(fw), rng.randrange(fh); dr.line([(x, y), (x + rng.randrange(2, 6), y + rng.randrange(-2, 3))], fill=(255, 255, 255, 70))
            elif st == "stone":
                for _ in range(max(2, area // 300)):
                    x, y = rng.randrange(fw), rng.randrange(fh)
                    for _ in range(rng.randrange(3, 7)):
                        nx, ny = x + rng.choice((-3, -1, 1, 3)), y + rng.randrange(1, 4); dr.line([(x, y), (nx, ny)], fill=(30, 28, 24, 190)); x, y = nx, ny
                for _ in range(area // 90):
                    x, y = rng.randrange(fw), rng.randrange(fh); r = rng.randrange(1, 3)
                    dr.ellipse([x, y, x + r, y + r], fill=(70, 110, 58, 90) if y > fh * 0.55 else _sh(col, 0.8) + (80,))
            elif st == "cloth":
                for k in range(-fh, fw, 7): dr.line([(k, 0), (k + fh // 2, fh)], fill=(0, 0, 0, 30), width=2)
                for xx in range(2, fw - 2, 4): dr.point((xx, 2), fill=_sh(col, 1.4) + (160,)); dr.point((xx, fh - 3), fill=_sh(col, 0.5) + (160,))
            else:
                for _ in range(area // 60): dr.point((rng.randrange(fw), rng.randrange(fh)), fill=_sh(col, 0.7) + (70,))
                for _ in range(max(1, area // 700)):
                    x, y = rng.randrange(fw), rng.randrange(fh); dr.arc([x, y, x + 6, y + 4], 0, 180, fill=_sh(col, 0.6) + (90,))
            if st in ("fur", "skin", "scale") and area > 300 and rng.random() < 0.35:  # battle scar
                x, y = rng.randrange(2, fw - 6), rng.randrange(2, fh - 6); dr.line([(x, y), (x + 5, y + 4)], fill=_sh(col, 1.5) + (200,)); dr.line([(x + 1, y), (x + 6, y + 4)], fill=_sh(col, 0.5) + (160,))
            gtile = Image.new("RGBA", (fw, fh), (0, 0, 0, 0)); gd = ImageDraw.Draw(gtile)
            if fname == "front" and "eyes" in p["f"] and fw >= 14:  # painted face
                eyec = hexc(palette["eye"]); ew = max(3, int(fw * 0.085)); eh = max(2, int(ew * 0.8)); ey = int(fh * 0.34)
                slit = st in ("scale", "fur") and sid not in ("bokoblin",)
                for side, ex in ((-1, int(fw * 0.27)), (1, int(fw * 0.73))):
                    dr.ellipse([ex - ew, ey - eh, ex + ew, ey + eh], fill=(20, 12, 12, 255))
                    dr.ellipse([ex - ew + 1, ey - eh + 1, ex + ew - 1, ey + eh - 1], fill=eyec + (255,))
                    gd.ellipse([ex - ew + 1, ey - eh + 1, ex + ew - 1, ey + eh - 1], fill=eyec + (255,))
                    if slit: dr.ellipse([ex - 1, ey - eh + 1, ex + 1, ey + eh - 1], fill=(8, 4, 4, 255))
                    else: dr.ellipse([ex - ew // 3, ey - eh // 2, ex + ew // 3, ey + eh // 2], fill=(10, 5, 5, 255))
                    dr.point((ex - ew // 2, ey - eh // 2), fill=(255, 255, 255, 255))
                    dr.polygon([(ex - ew - 1, ey - eh - 1 + (3 if side < 0 else 0)), (ex + ew + 1, ey - eh - 1 + (0 if side < 0 else 3)), (ex + ew + 1, ey - eh + 2), (ex - ew - 1, ey - eh + 2)], fill=_sh(col, 0.35) + (230,))  # brow
                    dr.line([(ex - ew - 2, ey - eh - 2 + (4 if side < 0 else 0)), (ex + ew + 2, ey - eh - 2 + (0 if side < 0 else 4))], fill=_sh(col, 0.3) + (255,), width=2)
                if fh >= 18:  # mouth with fangs
                    my = int(fh * 0.84)
                    dr.line([(int(fw * 0.22), my), (int(fw * 0.78), my)], fill=(25, 10, 10, 255), width=2)
                    for tx in range(int(fw * 0.25), int(fw * 0.76), 5):
                        big = tx < int(fw * 0.3) or tx > int(fw * 0.7)
                        dr.polygon([(tx, my), (tx + 3, my), (tx + 1, my + (5 if big else 3))], fill=(240, 236, 220, 255))
            if fname == "front" and "nostrils" in p["f"] and fw >= 8:
                for nx in (int(fw * 0.28), int(fw * 0.72)):
                    dr.ellipse([nx - 2, fh - 6, nx + 2, fh - 2], fill=_sh(col, 0.25) + (255,)); dr.arc([nx - 3, fh - 7, nx + 3, fh - 1], 200, 340, fill=_sh(col, 1.4) + (200,))
            special(sid, p, fname, dr, gd, fw, fh, palette, rng)
            img.alpha_composite(tile, (fx, fy)); glow.alpha_composite(gtile, (fx, fy))
    px = img.load(); gp = glow.load()
    for x, y, c in saved: px[x, y] = c; gp[x, y] = c  # keep original emissive pixels crisp


def gen_species():
    os.makedirs(f"{A}/specs", exist_ok=True)
    os.makedirs(f"{A}/textures/entity", exist_ok=True)
    gen_damage()
    for sid, sp in SPECIES.items():
        parts = order_parts([dict(q) for q in sp["parts"]])
        if sid in DETAIL:
            parts += detail_extras(parts)
            parts = order_parts(parts); _ref = refine_geometry(parts)
            try: _sp = split_limbs(parts + _ref); pack(order_parts([dict(q) for q in _sp])); parts = [q for q in _sp if q in _sp]; _ref = []
            except AssertionError: print("limb split skipped for", sid)
            try:
                pack(order_parts([dict(q) for q in parts + _ref])); parts += _ref
            except AssertionError: print("refine skipped for", sid)
        parts = order_parts(parts)
        if sid in RANK_EXTRA: parts += rank_extras(parts)
        if sid in ("lynel", "stalhound", "shadow_beast", "dodongo", "helmasaur"):
            try: _q = split_limbs(parts, ("frontRightLeg", "frontLeftLeg", "backRightLeg", "backLeftLeg")); pack(order_parts([dict(q) for q in _q])); parts = _q
            except AssertionError: print("quad split skipped for", sid)
        if sid in ROUND and ROUND[sid]:
            rp = roundify([dict(q) for q in parts], ROUND[sid])
            try: pack(order_parts([dict(q) for q in rp])); parts = rp
            except AssertionError: print("round skipped for", sid)
        parts = order_parts(parts)
        try: pack(parts)
        except AssertionError:  # too many boxes for the 128px sheet: drop the optional refinement boxes
            drop = {q["n"] for q in refine_geometry(parts)}; parts = [q for q in parts if q["n"] not in drop]; print("dropped refinement for", sid); pack(parts)
        json.dump(dict(tex=[TEX, TEX], hunch=sp["hunch"], splay=sp.get("splay", 0), crouch=sp.get("crouch", 0), parts=parts),
                  open(f"{A}/specs/{sid}.json", "w"), separators=(",", ":"))
        for ri, rname in enumerate(RANKS):
            palette = PAL[sid][ri]
            img = Image.new("RGBA", (TEX, TEX), (0, 0, 0, 0)); glow = Image.new("RGBA", (TEX, TEX), (0, 0, 0, 0))
            rng = random.Random(zlib.crc32((sid + rname).encode()))
            for p in parts:
                paint_box(img, p, hexc(palette[p["c"]]), rng, palette)
                glow_pass(img, glow, p, sid, palette)
                style_pass(img, glow, p, sid, rng, palette)
            if sid in ALPHA:
                px = img.load()
                for x in range(TEX):
                    for y in range(TEX):
                        r_, g_, b_, a_ = px[x, y]
                        if a_: px[x, y] = (r_, g_, b_, ALPHA[sid])
            img = img.resize((TEX * 2, TEX * 2), Image.NEAREST); glow = glow.resize((TEX * 2, TEX * 2), Image.NEAREST)
            paint2x(img, glow, parts, sid, palette, zlib.crc32((sid + rname + "p").encode()))
            px2, gl2 = img.load(), glow.load(); r2 = random.Random(zlib.crc32((sid + rname + "2x").encode()))
            for x in range(TEX * 2):
                for y in range(TEX * 2):
                    r_, g_, b_, a_ = px2[x, y]
                    if a_ and not gl2[x, y][3]:  # micro noise + soft vertical shading inside each texel
                        f = 1 + r2.uniform(-0.035, 0.035) + ((y % 2) * 0.012 - 0.006) + ((x % 2) * 0.008 - 0.004)
                        px2[x, y] = (max(0, min(255, int(r_ * f))), max(0, min(255, int(g_ * f))), max(0, min(255, int(b_ * f))), a_)
            # 3x density for the enlarged creatures: smooth upscale + fine grain / fibre detail
            big = img.resize((TEX * 3, TEX * 3), Image.BICUBIC).filter(ImageFilter.UnsharpMask(radius=1.2, percent=70, threshold=2))
            bp = big.load(); r3 = random.Random(zlib.crc32((sid + rname + "3x").encode()))
            gb = glow.resize((TEX * 3, TEX * 3), Image.BICUBIC); gbp = gb.load(); st3 = STYLE.get(sid, "skin")
            for _ in range(TEX * TEX * 9 // 40):
                x, y = r3.randrange(TEX * 3), r3.randrange(TEX * 3); c0 = bp[x, y]
                if c0[3] < 200 or gbp[x, y][3] > 40: continue
                f = r3.choice((0.9, 0.94, 1.07, 1.12)); L = r3.randrange(2, 5)
                for k in range(L):
                    yy = y + k if st3 in ("fur", "skin", "cloth") else y; xx = x + (k if st3 in ("scale", "metal", "stone", "bone") else 0)
                    if yy < TEX * 3 and xx < TEX * 3 and bp[xx, yy][3] > 200 and gbp[xx, yy][3] < 40:
                        r_, g_, b_, a_ = bp[xx, yy]; bp[xx, yy] = (min(255, int(r_ * f)), min(255, int(g_ * f)), min(255, int(b_ * f)), a_)
            big.save(f"{A}/textures/entity/{sid}_{rname}.png", optimize=True)
            gb.save(f"{A}/textures/entity/{sid}_{rname}_glow.png", optimize=True)


# ---------------------------------------------------------------- weapons
# id, en, ja, kind, dmg bonus (added to base 1), durability, c1, c2
W = [
    ("boko_club", "Boko Club", "ボコ棍棒", "club", 3, 20, "#9a6a35", "#6a431f"),
    ("spiked_boko_club", "Spiked Boko Club", "トゲボコ棍棒", "club", 5, 30, "#9a6a35", "#b0b0b8"),
    ("dragonbone_boko_club", "Dragonbone Boko Club", "竜骨のボコ棍棒", "club", 8, 50, "#e8dcb8", "#b8a878"),
    ("boko_bat", "Boko Bat", "ボコバット", "club", 2, 18, "#c9a46a", "#8a6a3a"),
    ("boko_spear", "Boko Spear", "ボコの槍", "spear", 3, 25, "#9a6a35", "#a8a8b0"),
    ("spiked_boko_spear", "Spiked Boko Spear", "トゲボコの槍", "spear", 5, 35, "#9a6a35", "#c8c8d0"),
    ("dragonbone_boko_spear", "Dragonbone Boko Spear", "竜骨のボコ槍", "spear", 8, 50, "#e8dcb8", "#f0e8d0"),
    ("moblin_club", "Moblin Club", "モリブリンの棍棒", "club", 6, 30, "#7a5a3a", "#4a3220"),
    ("spiked_moblin_club", "Spiked Moblin Club", "トゲモリブリン棍棒", "club", 9, 45, "#7a5a3a", "#b0b0b8"),
    ("dragonbone_moblin_club", "Dragonbone Moblin Club", "竜骨のモリブリン棍棒", "club", 12, 70, "#e8dcb8", "#b8a878"),
    ("boko_bow", "Boko Bow", "ボコの弓", "bow", 3, 60, "#9a6a35", "#e8e0c8"),
    ("spiked_boko_bow", "Spiked Boko Bow", "トゲボコの弓", "bow", 5, 80, "#9a6a35", "#c8c8d0"),
    ("dragonbone_boko_bow", "Dragonbone Boko Bow", "竜骨のボコ弓", "bow", 8, 100, "#e8dcb8", "#f0f0e0"),
    ("travelers_bow", "Traveler's Bow", "旅人の弓", "bow", 4, 70, "#8a6a3a", "#e8e0c8"),
    ("soldiers_bow", "Soldier's Bow", "兵士の弓", "bow", 6, 90, "#8a6a3a", "#d4d8e0"),
    ("knights_bow", "Knight's Bow", "騎士の弓", "bow", 9, 110, "#4a6aa8", "#e0e4ec"),
    ("royal_bow", "Royal Bow", "王家の弓", "bow", 12, 140, "#d8b43a", "#f0f2f8"),
    ("lynel_bow", "Lynel Bow", "ライネルの弓", "bow", 12, 100, "#8a4a3a", "#d8a85a"),
    ("mighty_lynel_bow", "Mighty Lynel Bow", "強ライネルの弓", "bow", 16, 130, "#3a6aa8", "#d8e0f0"),
    ("savage_lynel_bow", "Savage Lynel Bow", "猛ライネルの弓", "bow", 21, 160, "#2a2a34", "#e8c85a"),
    ("yiga_blade", "Yiga Blade", "イーガ団の刀", "sword", 6, 60, "#c0c4cc", "#9a1e1e"),
    ("yiga_bow", "Yiga Bow", "イーガ団の弓", "bow", 6, 90, "#3a2a2a", "#9a1e1e"),
    ("boko_shield", "Boko Shield", "ボコ盾", "shield", 0, 60, "#9a6a35", "#6a431f"),
    ("spiked_boko_shield", "Spiked Boko Shield", "トゲボコ盾", "shield", 0, 90, "#9a6a35", "#b0b0b8"),
    ("dragonbone_boko_shield", "Dragonbone Boko Shield", "竜骨のボコ盾", "shield", 0, 130, "#e8dcb8", "#b8a878"),
    ("soldiers_shield", "Soldier's Shield", "兵士の盾", "shield", 0, 100, "#8a8e98", "#8a6a3a"),
    ("knights_shield", "Knight's Shield", "騎士の盾", "shield", 0, 150, "#4a6aa8", "#e0e4ec"),
    ("royal_shield", "Royal Shield", "王家の盾", "shield", 0, 200, "#d8b43a", "#f0f2f8"),
    ("hylian_shield", "Hylian Shield", "ハイリアの盾", "shield", 0, 400, "#2a4a9a", "#d8b43a"),
    ("guardian_sword", "Guardian Sword", "ガーディアンソード", "sword", 14, 120, "#4ac8ff", "#2a6a9a"),
    ("guardian_sword_plus", "Guardian Sword++", "ガーディアンソード++", "claymore", 22, 160, "#4ac8ff", "#2a6a9a"),
    ("guardian_spear", "Guardian Spear", "ガーディアンスピア", "spear", 14, 120, "#2a6a9a", "#4ac8ff"),
    ("guardian_shield", "Guardian Shield", "ガーディアンシールド", "shield", 0, 300, "#4a6a78", "#ff7a20"),
    ("stalfos_sword", "Stalfos Sword", "スタルフォスの剣", "sword", 6, 70, "#d8d4c0", "#6a4a3a"),
    ("stalmaster_sword", "Stalmaster Greatsword", "スタルマスターの大剣", "claymore", 12, 120, "#c8c4b0", "#5a3a6a"),
        ("armos_sword", "Armos Blade", "アーモスの剣", "claymore", 10, 110, "#9a9a8a", "#6a6a5a"),
    ("ghirahim_sword", "Ghirahim's Sword", "ギラヒムの剣", "sword", 16, 200, "#f4f4f8", "#3a2a5a"),
    ("demise_sword", "Demise's Greatsword", "魔王の大剣", "claymore", 26, 300, "#3a2a2a", "#d83a20"),
    ("koloktos_sword", "Koloktos Scimitar", "コロクトスの曲刀", "claymore", 14, 140, "#c8a850", "#7a5a20"),
    ("stalfos_shield", "Stalfos Shield", "スタルフォスの盾", "shield", 0, 120, "#c8c4b0", "#6a4a3a"),
        ("don_cutlass", "Dreadfull Cutlass", "ドン・ゲラーのカトラス", "sword", 12, 150, "#c8ccd4", "#d8b840"),
    ("bulblin_club", "Bulblin Club", "ブルブリンの棍棒", "club", 5, 40, "#8a5a35", "#5a3a20"),
    ("bulblin_spear", "Bulblin Spear", "ブルブリンの槍", "spear", 5, 45, "#8a5a35", "#b0b0b8"),
    ("bulblin_bow", "Bulblin Bow", "ブルブリンの弓", "bow", 5, 80, "#7a4a28", "#e0d8c0"),
    ("bulblin_shield", "Bulblin Shield", "ブルブリンの盾", "shield", 0, 100, "#8a5a35", "#6a3a20"),
    ("king_bulblin_club", "King Bulblin's Club", "ブルブリン王の大棍棒", "claymore", 16, 140, "#6a4a30", "#c8a850"),
    ("dinolfos_sword", "Dinolfos Sword", "ディノルフォスの剣", "sword", 9, 90, "#a8b0b8", "#8a3a2a"),
    ("dinolfos_shield", "Dinolfos Shield", "ディノルフォスの盾", "shield", 0, 160, "#8a9aa8", "#8a3a2a"),
    ("aeralfos_spear", "Aeralfos Spear", "エアロルフォスの槍", "spear", 9, 90, "#7a5a3a", "#c8c8d0"),
    ("dark_nut_sword", "Dark Nut Greatsword", "ダークナットの大剣", "claymore", 18, 200, "#3a3a44", "#d83a3a"),
    ("dark_nut_shield", "Dark Nut Shield", "ダークナットの盾", "shield", 0, 300, "#3a3a44", "#8a2a2a"),
    ("death_sword_blade", "Death Sword Blade", "デスソードの大剣", "claymore", 24, 300, "#5a4a6a", "#c8c0e0"),
    ("zant_sword", "Zant's Scimitar", "ザントの曲刀", "sword", 14, 200, "#8a8aa0", "#2a2a3a"),
    ("ganon_sword", "Ganondorf's Greatsword", "ガノンドロフの大剣", "claymore", 24, 300, "#4a3a3a", "#d8a020"),
    ("fyrus_blade", "Fyrus Scimitar", "ファイラスの曲刀", "claymore", 22, 250, "#d86a20", "#4a2a1a"),
    ("lizal_boomerang", "Lizal Boomerang", "リザルブーメラン", "boomerang", 5, 30, "#7a9a3a", "#e0d08a"),
    ("lizal_forked_boomerang", "Lizal Forked Boomerang", "リザルフォーク", "boomerang", 7, 40, "#3a8ac0", "#bfe0ee"),
    ("lizal_tri_boomerang", "Lizal Tri-Boomerang", "リザルトライブーメラン", "boomerang", 10, 60, "#4a4a5a", "#aaaabb"),
    ("travelers_sword", "Traveler's Sword", "旅人の剣", "sword", 3, 40, "#c8ccd4", "#7a5a3a"),
    ("soldiers_broadsword", "Soldier's Broadsword", "兵士の剣", "sword", 5, 50, "#d4d8e0", "#8a6a3a"),
    ("knights_broadsword", "Knight's Broadsword", "騎士の剣", "sword", 8, 70, "#e0e4ec", "#4a6aa8"),
    ("royal_broadsword", "Royal Broadsword", "王家の剣", "sword", 11, 90, "#f0f2f8", "#d8b43a"),
    ("royal_guards_sword", "Royal Guard's Sword", "王家の近衛の剣", "sword", 13, 100, "#f4f6fa", "#2a4a9a"),
    ("zora_sword", "Zora Sword", "ゾーラの剣", "sword", 5, 45, "#9ad0e8", "#e8f4fa"),
    ("gerudo_scimitar", "Gerudo Scimitar", "ゲルド族のシミター", "sword", 8, 60, "#d8c078", "#a8782a"),
    ("lynel_sword", "Lynel Sword", "ライネルの剣", "sword", 12, 80, "#8a4a3a", "#d8a85a"),
    ("mighty_lynel_sword", "Mighty Lynel Sword", "強ライネルの剣", "sword", 16, 100, "#3a6aa8", "#d8e0f0"),
    ("savage_lynel_sword", "Savage Lynel Sword", "猛ライネルの剣", "sword", 21, 130, "#2a2a34", "#e8c85a"),
    ("master_sword", "Master Sword", "マスターソード", "sword", 14, 400, "#cfe8ff", "#2a3a9a"),
    ("travelers_claymore", "Traveler's Claymore", "旅人の大剣", "claymore", 6, 40, "#c8ccd4", "#7a5a3a"),
    ("soldiers_claymore", "Soldier's Claymore", "兵士の大剣", "claymore", 9, 55, "#d4d8e0", "#8a6a3a"),
    ("knights_claymore", "Knight's Claymore", "騎士の大剣", "claymore", 13, 75, "#e0e4ec", "#4a6aa8"),
    ("royal_claymore", "Royal Claymore", "王家の大剣", "claymore", 17, 100, "#f0f2f8", "#d8b43a"),
    ("lynel_crusher", "Lynel Crusher", "ライネルクラッシャー", "club", 13, 60, "#8a4a3a", "#d8a85a"),
    ("mighty_lynel_crusher", "Mighty Lynel Crusher", "強ライネルクラッシャー", "club", 17, 80, "#3a6aa8", "#d8e0f0"),
    ("savage_lynel_crusher", "Savage Lynel Crusher", "猛ライネルクラッシャー", "club", 22, 100, "#2a2a34", "#e8c85a"),
    ("travelers_spear", "Traveler's Spear", "旅人の槍", "spear", 4, 40, "#8a6a3a", "#c8ccd4"),
    ("soldiers_spear", "Soldier's Spear", "兵士の槍", "spear", 6, 50, "#8a6a3a", "#d4d8e0"),
    ("knights_halberd", "Knight's Halberd", "騎士のハルバード", "halberd", 9, 70, "#4a6aa8", "#e0e4ec"),
    ("royal_halberd", "Royal Halberd", "王家のハルバード", "halberd", 12, 90, "#d8b43a", "#f0f2f8"),
    ("lynel_spear", "Lynel Spear", "ライネルの槍", "spear", 12, 80, "#8a4a3a", "#d8a85a"),
    ("mighty_lynel_spear", "Mighty Lynel Spear", "強ライネルの槍", "spear", 16, 100, "#3a6aa8", "#d8e0f0"),
    ("savage_lynel_spear", "Savage Lynel Spear", "猛ライネルの槍", "spear", 21, 130, "#2a2a34", "#e8c85a"),
]


def line(d, a, b, col, w=1):
    d.line([a, b], fill=col, width=w)


def item_tex(kind, c1, c2, name):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    a, b = hexc(c1) + (255,), hexc(c2) + (255,)
    dk = shade(hexc(c2), 0.6) + (255,)
    if kind in ("sword", "claymore"):
        wdt = 3 if kind == "claymore" else 2
        line(d, (4, 11), (13, 2), a, wdt)
        line(d, (5, 11), (13, 3), shade(hexc(c1), 1.2) + (255,), 1)
        line(d, (3, 9), (7, 13), b, 2)
        line(d, (1, 14), (3, 12), dk, 2)
    elif kind == "club":
        line(d, (2, 14), (9, 7), b, 2)
        d.ellipse([7, 1, 13, 7], fill=a)
        d.ellipse([8, 2, 11, 5], fill=shade(hexc(c1), 1.2) + (255,))
        if "spiked" in name or "dragonbone" in name or "crusher" in name:
            for p in [(6, 3), (7, 0), (13, 3), (12, 0), (14, 6), (9, 8), (6, 6)]:
                d.point(p, fill=b if "spiked" in name else shade(hexc(c1), 0.8) + (255,))
    elif kind in ("spear", "halberd"):
        line(d, (1, 14), (11, 4), a, 1)
        line(d, (11, 4), (14, 1), b, 2)
        d.polygon([(10, 2), (14, 1), (13, 5)], fill=b)
        if kind == "halberd":
            d.polygon([(8, 5), (4, 3), (7, 8)], fill=b)
    elif kind == "shield":
        d.polygon([(3, 2), (12, 2), (13, 8), (8, 14), (2, 8)], fill=a, outline=dk)
        d.line([(8, 3), (8, 13)], fill=b, width=2); d.line([(4, 7), (11, 7)], fill=b, width=1)
    elif kind == "bow":
        d.arc([-6, 1, 13, 20], 270, 90, fill=a, width=2)
        line(d, (7, 1), (7, 14), b, 1)
        d.point((8, 7), fill=dk)
    elif kind == "boomerang":
        d.arc([2, 2, 14, 14], 200, 340, fill=a, width=3)
        d.arc([2, 2, 14, 14], 190, 350, fill=b, width=1)
        d.point((2, 8), fill=a); d.point((13, 8), fill=a)
    return im


SHOTS = {"shot_rock": ("Rock", "岩", "#8a8478"), "shot_fire": ("Fireball", "火球", "#ff7a2a"),
         "shot_ice": ("Ice Ball", "氷塊", "#9ae0ff"), "shot_elec": ("Spark Ball", "雷球", "#ffee44")}


def gen_shots():
    for i, (en, ja, c) in SHOTS.items():
        im = Image.new("RGBA", (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse([3, 3, 12, 12], fill=hexc(c) + (255,), outline=shade(hexc(c), .6) + (255,))
        d.ellipse([5, 5, 8, 8], fill=shade(hexc(c), 1.3) + (255,))
        im.save(f"{A}/textures/item/{i}.png")
        json.dump({"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{i}"}}, open(f"{A}/models/item/{i}.json", "w"))


def enhance(im):
    """16x16 -> 32x32 with dark outline and top-left highlight."""
    big = im.resize((32, 32), Image.NEAREST); px = big.load(); out = big.copy(); o = out.load()
    for x in range(32):
        for y in range(32):
            if px[x, y][3] == 0:
                if any(0 <= x + dx < 32 and 0 <= y + dy < 32 and px[x + dx, y + dy][3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): o[x, y] = (20, 16, 24, 255)
            else:
                r, g, b, a = px[x, y]
                up, left = (y > 0 and px[x, y - 1][3] == 0), (x > 0 and px[x - 1, y][3] == 0)
                f = 1.18 if (up or left) else (0.84 if ((y < 31 and px[x, y + 1][3] == 0) or (x < 31 and px[x + 1, y][3] == 0)) else 1.0)
                o[x, y] = (min(255, int(r * f)), min(255, int(g * f)), min(255, int(b * f)), a)
    return out


def gen_weapons():
    os.makedirs(f"{A}/textures/item", exist_ok=True)
    os.makedirs(f"{A}/models/item", exist_ok=True)
    wj = []
    for (i, en, ja, kind, dmg, dur, c1, c2) in W:
        enhance(item_tex(kind, c1, c2, i)).save(f"{A}/textures/item/{i}.png")
        if kind == "bow":
            base = item_tex(kind, c1, c2, i)
            for k in range(3):  # pulling_0..2: arrow nocked, string drawn back
                im = base.copy(); dd = ImageDraw.Draw(im)
                dd.line([(7, 1), (7 - k - 1, 7), (7, 14)], fill=(235, 235, 225, 255), width=1)
                dd.line([(2 + k * 2, 8), (13, 8)], fill=(150, 110, 60, 255), width=1); dd.point((13, 7), fill=(200, 200, 210, 255)); dd.point((13, 9), fill=(200, 200, 210, 255))
                enhance(im).save(f"{A}/textures/item/{i}_pulling_{k}.png")
                json.dump({"parent": "minecraft:item/handheld", "textures": {"layer0": f"{MOD}:item/{i}_pulling_{k}"}}, open(f"{A}/models/item/{i}_pulling_{k}.json", "w"))
            json.dump({"parent": "minecraft:item/handheld", "textures": {"layer0": f"{MOD}:item/{i}"}, "overrides": [
                {"predicate": {"pulling": 1}, "model": f"{MOD}:item/{i}_pulling_0"},
                {"predicate": {"pulling": 1, "pull": 0.65}, "model": f"{MOD}:item/{i}_pulling_1"},
                {"predicate": {"pulling": 1, "pull": 0.9}, "model": f"{MOD}:item/{i}_pulling_2"}]}, open(f"{A}/models/item/{i}.json", "w"))
        elif kind == "shield":
            tex = {"layer0": f"{MOD}:item/{i}"}
            json.dump({"parent": "minecraft:item/handheld", "textures": tex, "display": {"thirdperson_righthand": {"rotation": [0, 90, 0], "translation": [0, 2, -3], "scale": [1.1, 1.1, 1.1]}, "thirdperson_lefthand": {"rotation": [0, 90, 0], "translation": [0, 2, -3], "scale": [1.1, 1.1, 1.1]}},
                       "overrides": [{"predicate": {"blocking": 1}, "model": f"{MOD}:item/{i}_blocking"}]}, open(f"{A}/models/item/{i}.json", "w"))
            json.dump({"parent": "minecraft:item/handheld", "textures": tex, "display": {
                "firstperson_righthand": {"rotation": [0, 90, -15], "translation": [-3, 4, 2], "scale": [1.5, 1.5, 1.5]}, "firstperson_lefthand": {"rotation": [0, 90, -15], "translation": [-3, 4, 2], "scale": [1.5, 1.5, 1.5]},
                "thirdperson_righthand": {"rotation": [0, 0, 0], "translation": [0, 3, -4], "scale": [1.3, 1.3, 1.3]}, "thirdperson_lefthand": {"rotation": [0, 0, 0], "translation": [0, 3, -4], "scale": [1.3, 1.3, 1.3]}}},
                      open(f"{A}/models/item/{i}_blocking.json", "w"))
        else:
            json.dump({"parent": "minecraft:item/handheld", "textures": {"layer0": f"{MOD}:item/{i}"}}, open(f"{A}/models/item/{i}.json", "w"))
        wj.append(dict(id=i, kind=kind, dmg=dmg, dur=dur))
    json.dump(wj, open(f"{A}/weapons.json", "w"), separators=(",", ":"))


NAMES = {"bokoblin": ("Bokoblin", "ボコブリン"), "moblin": ("Moblin", "モリブリン"),
         "lizalfos": ("Lizalfos", "リザルフォス"), "keese": ("Keese", "キース"), "hinox": ("Hinox", "ヒノックス"), "talus": ("Talus", "イワロック"),
         "gibdo": ("Gibdo", "ガイブドー"), "horriblin": ("Horriblin", "ホラブリン"),
         "stalfos": ("Stalfos", "スタルフォス"), "stalmaster": ("Stalmaster", "スタルマスター"), "dark_lizalfos": ("Dark Lizalfos", "ヤミリザルフォス"), 
         "armos": ("Armos", "アモス"), "beamos": ("Beamos", "ビーモス"), "skulltula": ("Staltula", "スタルチュラ"), "deku_baba": ("Deku Baba", "デクババ"),
         "cursed_bokoblin": ("Rotten Bokoblin", "くされボコブリン"), "ghirahim": ("Ghirahim", "魔族長 ギラヒム"), "demise": ("Demise", "終焉の者"), "moldarach": ("Moldarach", "千年甲殻蟲 モルドガット"),
         "koloktos": ("Koloktos", "魔触神器 ダ・イルオーマ"), "scaldera": ("Scaldera", "獄炎大岩 ベラ・ダーマ"), "the_imprisoned": ("The Imprisoned", "封印されしもの"), "tentalus": ("Tentalus", "古代海獣 ダイダゴス"),
         "bulblin": ("Bulblin", "ブルブリン"), "king_bulblin": ("King Bulblin", "ブルブリン王"), "stalhound": ("Stalhound", "スタルハウンド"), "shadow_beast": ("Shadow Beast", "影の獣"),
         "redead": ("Redead", "リーデッド"), "poe": ("Poe", "ポウ"), "tektite": ("Tektite", "テクタイト"), "peahat": ("Peahat", "ピーハット"),
         "bubble_fire": ("Fire Bubble", "ファイアバブル"), "bubble_ice": ("Ice Bubble", "アイスバブル"), "bubble_dark": ("Cursed Bubble", "呪いのバブル"),
         "dodongo": ("Dodongo", "ドドンゴ"), "helmasaur": ("Helmasaur", "ヘルマサウルス"), "dark_nut": ("Dark Nut", "ダークナット"), "death_sword": ("Death Sword", "デスソード"),
         "zant": ("Zant", "ザント"), "ganondorf": ("Ganondorf", "ガノンドロフ"), "diababa": ("Diababa", "ディアババ"), "argorok": ("Argorok", "アルゴロック"), "fyrus": ("Fyrus", "ファイラス"),
         "armogohma": ("Armogohma", "アルモゴーマ"), "aeralfos": ("Aeralfos", "エアロルフォス"), "dinolfos": ("Dinolfos", "ディノルフォス"), "kargarok": ("Kargarok", "カーガロック"),
         "techno_bokoblin": ("Techno Bokoblin", "テクノボコブリン"), "quadro_baba": ("Quadro Baba", "ヨツババ"), "keese_dark": ("Dark Keese", "ヤミキース"),
         "wall_skulltula": ("Wall Staltula", "スタルウォール"), "petit_moldorm": ("Petit Moldorm", "プチガット"), "shakomite": ("Shakomite", "シャコマイト"),
         "frog_magma": ("Magpo", "マグッポ"), "frog_elec": ("Bilipo", "ビリッポ"), "frog_dark": ("Yamipo", "ヤミッポ"), "frog_water": ("Mizupo", "ミズッポ"),
         "don_gerar": ("Dreadfull Gerar", "ドン・ゲラー"), "don_killer": ("Dreadfull Killer", "ドン・キラー"), "gumarm": ("Magmarm", "グマーム"), "paraspalas": ("Parasparus", "巨眼寄生種 パラスパラス"),
         "lizalfos_fire": ("Fire Breath Lizalfos", "火吹きリザルフォス"), "lizalfos_ice": ("Ice Breath Lizalfos", "雹吐きリザルフォス"), "lizalfos_elec": ("Shock Lizalfos", "シビレリザルフォス"),
         "keese_fire": ("Fire Keese", "ファイアキース"), "keese_ice": ("Ice Keese", "アイスキース"), "keese_elec": ("Thunder Keese", "サンダーキース"),
         "octorok": ("Octorok", "オクタロック"), "wizzrobe": ("Wizzrobe", "ウィズローブ"), "blizzrobe": ("Blizzrobe", "フリーズウィズローブ"), "thunder_wizzrobe": ("Thunder Wizzrobe", "ボルトウィズローブ"),
         "lynel": ("Lynel", "ライネル"), "chuchu": ("Chuchu", "チュチュ"), "guardian": ("Guardian Stalker", "ガーディアン"), "decayed_guardian": ("Decayed Guardian", "朽ちたガーディアン"),
         "guardian_turret": ("Guardian Turret", "ガーディアン・タレット"), "guardian_skywatcher": ("Guardian Skywatcher", "ガーディアン・スカイウォッチャー"),
         "guardian_scout_1": ("Guardian Scout I", "ガーディアン・スカウトI"), "guardian_scout_2": ("Guardian Scout II", "ガーディアン・スカウトII"),
         "guardian_scout_3": ("Guardian Scout III", "ガーディアン・スカウトIII"), "guardian_scout_4": ("Guardian Scout IV", "ガーディアン・スカウトIV"),
         "stalkoblin": ("Stalkoblin", "スタルコブリン"), "stalmoblin": ("Stalmoblin", "スタルモリブリン"), "stalizalfos": ("Stalizalfos", "スタルリザルフォス"),
         "yiga_footsoldier": ("Yiga Footsoldier", "イーガ団員"), "yiga_blademaster": ("Yiga Blademaster", "イーガ団の剣士"),
         "soldier_construct": ("Soldier Construct", "ソルジャーコンストラクト"), "captain_construct": ("Captain Construct", "キャプテンコンストラクト"),
         "frox": ("Frox", "フロックス"), "stalhinox": ("Stalhinox", "スタルヒノックス"), "calamity_ganon": ("Calamity Ganon", "厄災ガノン"),
         "master_kohga": ("Master Kohga", "マスター・コーガ"), "fireblight_ganon": ("Fireblight Ganon", "炎のカースガノン"),
         "waterblight_ganon": ("Waterblight Ganon", "水のカースガノン"), "windblight_ganon": ("Windblight Ganon", "風のカースガノン"),
         "thunderblight_ganon": ("Thunderblight Ganon", "雷のカースガノン"), "phantom_ganon": ("Phantom Ganon", "ファントムガノン"), "gleeok": ("Gleeok", "ゴーマ")}
RANK_EN = [r.capitalize() for r in RANKS]


def gen_lang():
    os.makedirs(f"{A}/lang", exist_ok=True)
    for code, idx in (("en_us", 0), ("ja_jp", 1)):
        L = {"itemGroup." + MOD: "Hyrule Creatures" if idx == 0 else "ハイラルの魔物"}
        L["itemGroup." + MOD + ".variants"] = "Hyrule Creatures: Variants" if idx == 0 else "ハイラルの魔物:色違い"
        for i, r in enumerate(RANKS):
            L[f"rank.{MOD}.{r}"] = RANK_EN[i] if idx == 0 else RANK_JA[i]
        for sid, n in NAMES.items():
            for suf, en, ja in (("horn", "Horn", "角"), ("fang", "Fang", "牙"), ("guts", "Guts", "内臓")):
                L[f"item.{MOD}.{sid}_{suf}"] = f"{n[0]} {en}" if idx == 0 else f"{n[1]}の{ja}"
            L[f"entity.{MOD}.{sid}"] = n[idx]
            L[f"item.{MOD}.{sid}_spawn_egg"] = n[idx] + (" Spawn Egg" if idx == 0 else "のスポーンエッグ")
        for i, (en, ja, c) in SHOTS.items():
            L[f"item.{MOD}.{i}"] = (en, ja)[idx]
        L[f"entity.{MOD}.shot"] = ("Projectile", "飛び道具")[idx]
        L[f"entity.{MOD}.stal_head"] = ("Stal Skull", "スタルの頭")[idx]
        for sid, n in NAMES.items():
            for r, rn in enumerate(RANKS):
                L[f"item.{MOD}.{sid}_{rn}_spawn_egg"] = (f"{RANK_EN[r]} {n[0]} Spawn Egg" if idx == 0 else f"{RANK_JA[r]}の{n[1]}のスポーンエッグ")
        for w in W:
            L[f"item.{MOD}.{w[0]}"] = w[1 + idx]
        json.dump(L, open(f"{A}/lang/{code}.json", "w"), ensure_ascii=False, indent=1)


def gen_parts():
    kinds = [("horn", "Horn", "角", 0.7), ("fang", "Fang", "牙", 0.5), ("guts", "Guts", "内臓", 0.3)]
    ld = os.path.join(RES, "data", MOD, "loot_tables", "entities"); os.makedirs(ld, exist_ok=True)
    for sid in SPECIES:
        pl = PAL[sid][0]
        for suf, en, ja, ch in kinds:
            im = Image.new("RGBA", (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            if suf == "horn":
                c = hexc(pl["horn"]) + (255,); d.polygon([(4, 14), (7, 3), (9, 3), (12, 14)], fill=c, outline=shade(hexc(pl["horn"]), .6) + (255,))
            elif suf == "fang":
                d.polygon([(5, 3), (11, 3), (8, 14)], fill=(240, 240, 232, 255), outline=(150, 150, 140, 255))
            else:
                d.ellipse([3, 4, 13, 12], fill=(200, 90, 110, 255), outline=(120, 40, 60, 255)); d.ellipse([5, 6, 8, 8], fill=(230, 140, 150, 255))
            im.save(f"{A}/textures/item/{sid}_{suf}.png")
            json.dump({"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{sid}_{suf}"}}, open(f"{A}/models/item/{sid}_{suf}.json", "w"))
        pools = [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{MOD}:{sid}_{suf}",
                  "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 1, "max": 2}}],
                  "conditions": [{"condition": "minecraft:random_chance", "chance": ch}]}]} for suf, en, ja, ch in kinds]
        json.dump({"type": "minecraft:entity", "pools": pools}, open(f"{ld}/{sid}.json", "w"))


def gen_eggs():
    from PIL import Image as I
    import json as J
    mdl = f"{A}/models/item"
    for sid, sp in SPECIES.items():
        parts = J.load(open(f"{A}/specs/{sid}.json"))["parts"]
        hp = next((q for q in parts if q["n"] == "head"), None) or next(q for q in parts if q["n"] == "body")
        u, v = hp["uv"]; w, h, d = [int(round(t)) for t in hp["box"][3:6]]
        for r, rn in enumerate(RANKS):
            tex = I.open(f"{A}/textures/entity/{sid}_{rn}.png").convert("RGBA")
            face = tex.crop((u + d, v + d, u + d + w, v + d + h)).resize((10, 10), I.NEAREST)
            base = hexc(PAL[sid][r]["skin"])
            egg = I.new("RGBA", (16, 16), (0, 0, 0, 0)); dr = ImageDraw.Draw(egg)
            _bc = [(220, 60, 50), (60, 110, 230), (40, 40, 50), (225, 228, 235), (240, 200, 60)][r]
            dr.ellipse([1, 0, 14, 15], fill=shade(base, 0.85) + (255,), outline=_bc + (255,))
            dr.ellipse([2, 1, 13, 14], outline=(20, 20, 20, 255))
            egg.alpha_composite(face, (3, 3))
            dr.arc([1, 0, 14, 15], 200, 340, fill=(255, 255, 255, 120))
            for name in ([f"{sid}_spawn_egg"] if r == 0 else []) + [f"{sid}_{rn}_spawn_egg"]:
                egg.save(f"{A}/textures/item/{name}.png")
                J.dump({"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{name}"}}, open(f"{mdl}/{name}.json", "w"))
    J.dump({sid: [[PAL[sid][r]["skin"], PAL[sid][r]["horn"]] for r in range(5)] for sid in SPECIES}, open(f"{A}/eggs.json", "w"))


def gen_data():
    d = os.path.join(RES, "data", MOD, "forge", "biome_modifier")
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d): os.remove(os.path.join(d, f))  # bosses (gleeok, phantom ganon, captain construct) are spawn-egg/command only
    spawns = {"bokoblin": (40, 2, 4), "moblin": (20, 1, 2), "lizalfos": (25, 1, 3), "keese": (30, 2, 4), "hinox": (4, 1, 1), "talus": (8, 1, 1), "gibdo": (14, 1, 3), "horriblin": (14, 2, 3), "octorok": (12, 1, 2), "wizzrobe": (6, 1, 1), "blizzrobe": (3, 1, 1), "thunder_wizzrobe": (3, 1, 1), "lynel": (3, 1, 1), "chuchu": (30, 2, 4), "guardian": (3, 1, 1), "decayed_guardian": (4, 1, 1), "stalkoblin": (10, 2, 3), "stalmoblin": (5, 1, 2), "stalizalfos": (6, 1, 2), "yiga_footsoldier": (6, 1, 3), "yiga_blademaster": (2, 1, 1), "soldier_construct": (4, 1, 2), "frox": (2, 1, 1), "stalfos": (6, 1, 2), "dark_lizalfos": (3, 1, 2), "bulblin": (8, 2, 4), "stalhound": (5, 1, 3), "redead": (4, 1, 2), "poe": (4, 1, 2), "tektite": (6, 1, 3), "peahat": (4, 1, 2), "bubble_fire": (3, 1, 2), "bubble_ice": (3, 1, 2), "bubble_dark": (3, 1, 2), "dodongo": (2, 1, 1), "helmasaur": (3, 1, 1), "dark_nut": (1, 1, 1), "aeralfos": (2, 1, 1), "dinolfos": (3, 1, 2), "kargarok": (3, 1, 2), "shadow_beast": (2, 1, 1), "techno_bokoblin": (3, 1, 2), "quadro_baba": (3, 1, 2), "keese_dark": (4, 1, 3), "wall_skulltula": (6, 2, 4), "petit_moldorm": (6, 3, 6), "shakomite": (3, 1, 2), "frog_magma": (3, 1, 1), "frog_elec": (3, 1, 1), "frog_dark": (3, 1, 1), "frog_water": (3, 1, 1), "armos": (2, 1, 1), "skulltula": (8, 1, 3), "deku_baba": (6, 1, 2), "cursed_bokoblin": (4, 1, 2), "lizalfos_fire": (4, 1, 2), "lizalfos_ice": (4, 1, 2), "lizalfos_elec": (4, 1, 2), "keese_fire": (6, 2, 3), "keese_ice": (6, 2, 3), "keese_elec": (6, 2, 3)}
    for sid, (wt, lo, hi) in spawns.items():
        json.dump({"type": "forge:add_spawns", "biomes": "#minecraft:is_overworld",
                   "spawners": {"type": f"{MOD}:{sid}", "weight": wt, "minCount": lo, "maxCount": hi}},
                  open(f"{d}/{sid}.json", "w"))


if __name__ == "__main__":
    gen_species(); gen_weapons(); gen_shots(); gen_parts(); gen_lang(); gen_eggs(); gen_data()
    print("ok", len(W), "weapons")
