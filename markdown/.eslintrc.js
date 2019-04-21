// This is a js file instead of a json file because you can't have comments ot json files.
module.exports = {
    "parser": "@typescript-eslint/parser",
    "extends":  [ "plugin:@typescript-eslint/recommended" ],
    "parserOptions": {
        "ecmaVersion": 2018,
        "sourceType": "module"
    },
    "rules": {
        // Do not enforce requiring explicitly return types for arrow functions. Arrow functions are often embedded
        // directly into other functions. Requiring that we explicitly declare its return type will make it mentally
        // more taxing to figure out what's going on. For example...
        //     array.filter(x => x === someValue)
        // vs
        //     array.filter((x): boolean => x === someValue)
        "@typescript-eslint/explicit-function-return-type": {
            "allowExpressions": true,
            "allowTypedFunctionExpressions": true
        },
        // If we explicitly used any, it means we want it.
        "@typescript-eslint/no-explicit-any": "off"
    }
}