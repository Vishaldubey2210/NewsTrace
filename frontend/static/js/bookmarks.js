// Bookmark and Pinned Journalists Local Store
const Bookmarks = {
    KEY: 'newstrace_pinned_journalists',
    getAll: () => JSON.parse(localStorage.getItem(Bookmarks.KEY) || '[]'),
    toggle: (journalistId, name) => {
        let items = Bookmarks.getAll();
        const exists = items.some(i => i.id === journalistId);
        if (exists) {
            items = items.filter(i => i.id !== journalistId);
        } else {
            items.push({ id: journalistId, name: name });
        }
        localStorage.setItem(Bookmarks.KEY, JSON.stringify(items));
        return !exists;
    }
};
