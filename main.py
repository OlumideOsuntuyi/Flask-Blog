from website import create_app
import pandas as pd

tweets = pd.read_csv('website/static/dataset/twitter_dataset.csv')
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)