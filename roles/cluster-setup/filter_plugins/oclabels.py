class FilterModule(object):
    def filters(self):
        return {'oclabels': self.oclabels}

    def oclabels(self, hostvar, cluster_group='nodes'):
        results = []
        for entry in hostvar:
            if 'labels' in hostvar[entry] and cluster_group in hostvar[entry]['group_names']:
                labels = ' '.join(['%s=""' % label for label in hostvar[entry]['labels']])
                label = "oc label node %s %s --overwrite" % (entry, labels)
                results.append(label)
        return results
