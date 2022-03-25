# Model updates

Application models (many of references, Patient, Care) are updated via 3rd party APIs. Model updates is pluggable. The
updates impleneteation is defined in the django app {meth}`updates`

## Update sources

Every update source is consists of components:

- **data_loader**: it's a function that loads data from the source and return generator of items.
- **transformers**: zero or more functions that transform the data. They are applied in the order they are defined.
- **model_updater**: it's a function that updates (or create) the model with the data.
- **post_operation**: zero or more functions that is called after the update.

```{note}
**transformers** and **model_updater** are applied to every data item.
```

## Default data_loader

{meth}`updates.common.loaders.references_loader` - loads references from the iCiselniky. Supports incremental updates.

## Default model_updater

{meth}`updates.common.updaters.simple_model_updater` - updates reference model of same type as the iCiselniky data.

## How to add/change update source

Update source is defined in the `settings.UPDATE_SOURCES` variable. Value of this variable is a dictionary where keys
are update source names and values are dictionaries with the following keys:

- `data_loader`: fully qualified name of the data_loader function.
- `transformers`: list of fully qualified names of the transformer functions.
- `model_updater`: fully qualified name of the model_updater function.
- `post_operation`: list of fully qualified names of the post_operation function.

After adding/updating new update source, you need to run {ref}`create_sources` django command to create/update the
appropriate {meth}`updates.models.Source`instance.

## The `updates` django app models

- {meth}`updates.models.Source` - update source model.
- {meth}`updates.models.Update` - this model is created for every update.
- {meth}`updates.models.ModelUpdate` - An update can updates multiple models. Therefor this model is used to store the
  model update information.

