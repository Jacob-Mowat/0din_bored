test:
	( \
		python3 main.py data_in.txt; \
		)

run-server:
	( \
		export FLASK_APP=app.py; \
		export FLASK_ENV=development; \
		flask run; \	
	)

clean-blocks:
	( \
		rm ./data_store/blocks/block_*; \
	)
