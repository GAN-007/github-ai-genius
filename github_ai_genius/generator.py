class ProjectGenerator:
    def create_django_marketplace(self, root, name='marketplace'):
        root = root / name
        root.mkdir(parents=True, exist_ok=True)
        target = root / 'README.md'
        target.write_text('# Marketplace\n', encoding='utf-8')
        return type('GeneratedProject', (), {'root': root, 'files': [target]})()
