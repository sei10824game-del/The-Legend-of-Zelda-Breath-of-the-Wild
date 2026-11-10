#!/usr/bin/env python3
"""Single source of truth for creature models, textures, weapons, item textures, lang.
Run: python3 tools/gen_assets.py   (writes into src/main/resources)"""
import json, os, random, zlib
from PIL import Image, ImageDraw

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


def P(n, p, box, pose, rot=(0, 0, 0), c="skin", f=None):
    return dict(n=n, p=p, box=list(box), pose=list(pose), rot=list(rot), c=c, f=f or [])


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
    """BotW Guardian Stalker: flat copper shell, turret head with big eye, 8 long bone-coloured legs."""
    parts = [
        P("body", None, (-9, -3, -9, 18, 7, 18), (0, 8, 0), f=["circuit"]),
        P("shell2", "body", (-7, -6, -7, 14, 3, 14), (0, 0, 0), c="skin2", f=["circuit"]),
        P("rim", "body", (-9.5, 3, -9.5, 19, 1, 19), (0, 0, 0), c="horn"),
        P("head", "body", (-5, -8, -5, 10, 8, 10), (0, -3, -2), c="skin", f=["circuit"]),
        P("cap", "head", (-3, -3, -3, 6, 3, 6), (0, -8, 0), c="skin2"),
        P("crest", "head", (-1, -5, -2, 2, 2, 4), (0, -8, 0), c="horn"),
        P("eyeCyl", "head", (-3, -6, -8, 6, 5, 3), (0, 0, 0), c="skin2", f=["bigeye"]),
        P("eyeRing", "head", (-4, -7, -6, 8, 7, 1), (0, 0, 0), c="horn"),
    ]
    if legs:
        parts += spider_legs(8, 10, 8, 1.0, 9, 9, math.pi / 8)
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

SPECIES["horriblin"] = SPECIES["bokoblin"]
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

def bone(eye): return pal("#e6e0cc", "#c4bca4", "#d0c8b0", "#bfb79c", "#f4f0e0", eye=eye)
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


def gen_species():
    os.makedirs(f"{A}/specs", exist_ok=True)
    os.makedirs(f"{A}/textures/entity", exist_ok=True)
    for sid, sp in SPECIES.items():
        parts = order_parts([dict(q) for q in sp["parts"]])
        pack(parts)
        json.dump(dict(tex=[TEX, TEX], hunch=sp["hunch"], parts=parts),
                  open(f"{A}/specs/{sid}.json", "w"), separators=(",", ":"))
        for ri, rname in enumerate(RANKS):
            palette = PAL[sid][ri]
            img = Image.new("RGBA", (TEX, TEX), (0, 0, 0, 0))
            rng = random.Random(zlib.crc32((sid + rname).encode()))
            for p in parts:
                paint_box(img, p, hexc(palette[p["c"]]), rng, palette)
            img.save(f"{A}/textures/entity/{sid}_{rname}.png")


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


def gen_weapons():
    os.makedirs(f"{A}/textures/item", exist_ok=True)
    os.makedirs(f"{A}/models/item", exist_ok=True)
    wj = []
    for (i, en, ja, kind, dmg, dur, c1, c2) in W:
        item_tex(kind, c1, c2, i).save(f"{A}/textures/item/{i}.png")
        json.dump({"parent": "minecraft:item/handheld", "textures": {"layer0": f"{MOD}:item/{i}"}},
                  open(f"{A}/models/item/{i}.json", "w"))
        wj.append(dict(id=i, kind=kind, dmg=dmg, dur=dur))
    json.dump(wj, open(f"{A}/weapons.json", "w"), separators=(",", ":"))


NAMES = {"bokoblin": ("Bokoblin", "ボコブリン"), "moblin": ("Moblin", "モリブリン"),
         "lizalfos": ("Lizalfos", "リザルフォス"), "keese": ("Keese", "キース"), "hinox": ("Hinox", "ヒノックス"), "talus": ("Talus", "イワロック"),
         "gibdo": ("Gibdo", "ガイブドー"), "horriblin": ("Horriblin", "ホラブリン"),
         "octorok": ("Octorok", "オクタロック"), "wizzrobe": ("Wizzrobe", "ウィズローブ"),
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


def gen_data():
    d = os.path.join(RES, "data", MOD, "forge", "biome_modifier")
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d): os.remove(os.path.join(d, f))  # bosses (gleeok, phantom ganon, captain construct) are spawn-egg/command only
    spawns = {"bokoblin": (40, 2, 4), "moblin": (20, 1, 2), "lizalfos": (25, 1, 3), "keese": (30, 2, 4), "hinox": (4, 1, 1), "talus": (8, 1, 1), "gibdo": (14, 1, 3), "horriblin": (14, 2, 3), "octorok": (12, 1, 2), "wizzrobe": (6, 1, 1), "lynel": (3, 1, 1), "chuchu": (30, 2, 4), "guardian": (3, 1, 1), "decayed_guardian": (4, 1, 1), "stalkoblin": (10, 2, 3), "stalmoblin": (5, 1, 2), "stalizalfos": (6, 1, 2), "yiga_footsoldier": (6, 1, 3), "yiga_blademaster": (2, 1, 1), "soldier_construct": (4, 1, 2), "frox": (2, 1, 1)}
    for sid, (wt, lo, hi) in spawns.items():
        json.dump({"type": "forge:add_spawns", "biomes": "#minecraft:is_overworld",
                   "spawners": {"type": f"{MOD}:{sid}", "weight": wt, "minCount": lo, "maxCount": hi}},
                  open(f"{d}/{sid}.json", "w"))


if __name__ == "__main__":
    gen_species(); gen_weapons(); gen_shots(); gen_parts(); gen_lang(); gen_data()
    print("ok", len(W), "weapons")
