## Описание датасетов

- train_data.csv - оригинальный набор данных.
- clear_data.csv - оригинальный набор данных после первичной предобработки.
- df_train.csv - выделенная обучающая выборка из clear_data.csv для задачи классификации по типу оборудования.
- .csv - выделенная тестовая выборка из clear_data.csv для задачи классификации по типу оборудования.
- df_2_train.csv - выделенная обучающая выборка из clear_data.csv для задачи классификации по точке отказа оборудования.
- df_2_test.csv - выделенная тестовая выборка из clear_data.csv для задачи классификации по точке отказа оборудования.
- data_balanced_by_equipment.csv - clear_data.csv с синтетическими данными для задачи классификации по типу оборудования.
- data_balanced_by_failure_point.csv - clear_data.csv с синтетическими данными для задачи классификации по точке отказа оборудования.
- df_train_balanced_by_equipment - df_train.csv с синтетическими данными для задачи классификации по точке отказа оборудования.
- df_train_balanced_by_failure_point.csv - df_2_train.csv с синтетическими данными для задачи классификации по точке отказа оборудования
- df_train_balanced_by_equipmen_embeded.csv - df_train_balanced_by_equipment.csv с векторизованным текстом.
- df_train_balanced_failure_point_embeded - df_train_balanced_by_failure_point.csv с векторизованным текстом.
- df_test_balanced_by_equipmen_embeded - df_test.csv с векторизованным текстом.
- df_test_balanced_failure_point_embeded - df_2_test.csv с векторизованным текстом.