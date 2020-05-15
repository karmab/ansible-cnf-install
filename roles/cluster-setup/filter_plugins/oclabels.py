class FilterModule(object):
    def filters(self):
        return {'oclabels': self.oclabels}

    def oclabels(self, hostvar):
        results = []
        for entry in hostvar:
            if 'labels' in hostvar[entry] and 'nodes' in hostvar[entry]['group_names']:
                labels = ' '.join(['%s=""' % label for label in hostvar[entry]['labels']])
                label = "oc label node %s %s" % (entry, labels)
                results.append(label)
        return results
