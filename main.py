from src.dispatch import dispatch_tasks

if __name__ == "__main__":
    results = dispatch_tasks()
    print(results[:10])