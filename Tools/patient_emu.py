import os
import copy
import json
from random import random

from Parsers import HpoParser, PhenotypeAnnotationsParser

class PatientEmulator():
    def __init__(self, ancestor_prob=0.5, noise_prob=0.5):
        self.hpos = HpoParser()
        self.anns = PhenotypeAnnotationsParser()
        self.eligibles = list(self.__build_eligibles(self.hpos, self.anns))
        self.ancestor_prob = ancestor_prob
        self.noise_prob = noise_prob

    def __build_eligibles(self, hpos, anns):
        eligibles = anns.get_hpos()
        for hpo in list(eligibles):
            for ancestor in self.hpos.get_ancestors(hpo):
                eligibles.add(ancestor)
        return eligibles

    def __random_hpos(self, count):
        hpos = []
        for n in range(count):
            ix = int(random() * len(self.eligibles))
            hpos.append(self.eligibles[ix])
        return hpos

    def __random_ancestor(self, hpo, prob):
        if random() <= prob:
            ancestors = self.hpos.get_ancestors(hpo)
            ix = int(random() * len(ancestors))
            return ancestors[ix]
        return hpo

    def __random_ancestors(self, hpos, prob):
        return [self.__random_ancestor(hpo, prob) for hpo in hpos]

    def get_condition(self, source, name, describe=False):
        cond = self.anns.get_source(source)[name]
        cond = copy.copy(cond)
        if describe: cond = self.describe(cond)
        return cond

    def emulate_condition(self, source, name, describe=False):
        cond = self.get_condition(source, name)
        hpos = self.__random_ancestors(cond['hpos'], self.ancestor_prob)
        hpos.extend(self.__random_hpos(int(len(hpos) * self.noise_prob)))
        cond['hpos'] = hpos
        if describe: cond = self.describe(cond)
        return cond

    def emulate_conditions(self, source, count=3, describe=False, patient_file=True):
        conds = {}
        for name in self.anns.get_source(source):
            real = self.get_condition(source, name, describe=describe)
            cond = {
                    'desc': real['desc'],
                    'hpos': real['hpos'],
                    'sims': []
                }
            for n in range(count):
                emul = self.emulate_condition(source, name, describe=describe)
                cond['sims'].append(emul['hpos'])
            conds[name] = cond

        return conds

    def describe(self, cond):
        hpdescs = []
        for hpo in cond['hpos']:
            hpdescs.append(self.hpos[hpo]['desc'])
        cond['hpo_descs'] = hpdescs
        return cond
