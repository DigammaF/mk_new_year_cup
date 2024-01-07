"""
	there's about 10^88 different scenarios
"""

import dataclasses
from dataclasses import dataclass
import random
from typing import Self

@dataclass
class Racer:
	name: str
	score: int
	total_score: int

	def clone(self) -> Self:
		return dataclasses.replace(self)
	
	@staticmethod
	def new(name: str, total_score: int) -> Self:
		return Racer(name, 0, total_score)

GRP_D: list[Racer] = [
	Racer.new("miko", 43),
	Racer.new("pekora", 35),
	Racer.new("hajime", 33),
	Racer.new("noel", 29),
	Racer.new("kaela", 27),
	Racer.new("irys", 22),
	Racer.new("baelz", 25),
	Racer.new("ririka", 21),
	Racer.new("aki", 14),
	Racer.new("mococo", 9),
	Racer.new("kobo", 5),
]

GRP_E: list[Racer] = [
	Racer.new("ina", 42),
	Racer.new("calliope", 33),
	Racer.new("mio", 33),
	Racer.new("koyori", 35),
	Racer.new("ollie", 22),
	Racer.new("roboco", 26),
	Racer.new("mumei", 22),
	Racer.new("raden", 17),
	Racer.new("ayame", 19),
	Racer.new("fuwawa", 9),
]

GRP_F: list[Racer] = [
	Racer.new("kronii", 34),
	Racer.new("lui", 39),
	Racer.new("towa", 35),
	Racer.new("matsuri", 23),
	Racer.new("bijou", 29),
	Racer.new("sora", 24),
	Racer.new("anya", 20),
	Racer.new("haato", 20),
	Racer.new("mel", 20),
	Racer.new("kanade", 6),
	Racer.new("ao", 4),
]

SCORE: list[int] = [15, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

def run_race(grp: list[Racer]):
	"""
		simulates one race and updates the scores of the racers
	"""
	random.shuffle(grp)

	for racer, score in zip(grp, SCORE):
		racer.score += score

def run_group(grp: list[Racer]):
	"""
		simulates the races and updates the scores of the racers,
		sorting the racers at the end
	"""
	run_race(grp)
	run_race(grp)
	run_race(grp)
	run_race(grp)
	grp.sort(key=lambda racer: racer.score, reverse=True)

def run_groups() -> list[Racer]:
	"""
		returns the list of players qualified for Tsuyo
	"""
	grp_d = [racer.clone() for racer in GRP_D]
	grp_e = [racer.clone() for racer in GRP_E]
	grp_f = [racer.clone() for racer in GRP_F]
	run_group(grp_d)
	run_group(grp_e)
	run_group(grp_f)
	qualified: list[Racer] = [grp_d[0], grp_e[0], grp_f[0]]
	contenders: list[Racer] = grp_d[1:] + grp_e[1:] + grp_f[1:]
	
	for racer in contenders:
		racer.total_score += racer.score

	contenders.sort(key=lambda racer: racer.total_score, reverse=True)
	qualified += contenders[:6]
	return qualified

def attempt() -> bool:
	"""
		returns true if Biboo qualifies for Tsuyo
	"""
	return any(racer.name == "bijou" for racer in run_groups())

def mainloop():
	attempts = 0
	tracked: dict[str, int] = {
		"bijou": 0,
		"kronii": 0,
		"ina": 0,
		"calliope": 0
	}
	names: list[str] = sorted(tracked)

	while True:
		attempts += 1
		qualified = run_groups()

		for racer in qualified:
			if racer.name in tracked:
				tracked[racer.name] += 1

		if attempts % 100_000 == 0:
			print(f"{attempts=}")

			for name in names:
				print(f"{name}: {tracked[name]/attempts:.3f}")

mainloop()
