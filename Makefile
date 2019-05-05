result.csv: clean.py raw.csv
	python $<
raw.csv: spider.py
	scrapy runspider $< -o $@

.PHONY: clean

clean:
	rm -f *.csv
