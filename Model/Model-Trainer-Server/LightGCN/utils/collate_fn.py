def train_make_collate_fn(samples):
    users = []
    pos_items = []
    neg_items = []
    for sample in samples:
        users += [sample['user']]
        pos_items += [sample['pos_item']]
        neg_items += [sample['neg_item']]
    return {
            'users' : users,
            'pos_items' : pos_items,
            'neg_items' : neg_items,
            }

def valid_make_collate_fn(samples):
    users = [sample['user'] for sample in samples]
    return users