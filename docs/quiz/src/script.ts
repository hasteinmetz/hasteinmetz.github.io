//to do:
// fix Tongan
// add country questions - Done
// add fun sounds - Done
// REFACTOR TO TYPESCRIPT

import { languages, country_js, lang_js, countries } from "../Contents/languages1";

interface jsonDataBase {
    speakers: string | null;
    difficulty: string | null;
    link: string | null;
    scripts: string[] | null;
    mainfam: string | null;
}

class JsonProblemKeys<T> {
    endonym: T | null = null;
    region: T | null = null;
    family: T | null = null;
    vplaces: T | null = null;
    vspeakers: T | null = null;
    official: T | null = null;
    places: T | null = null;
}

type LanguageJsonDataRaw = jsonDataBase & JsonProblemKeys<string | string[]>
type LanguageJsonData = jsonDataBase & JsonProblemKeys<string[]>;
type LanguageJsonRecordRaw = {[key: string]: LanguageJsonDataRaw};

interface LanguageJsonRecord extends LanguageJsonData {
    name: string
}

function fixJsonDataProperty(languageJson: LanguageJsonDataRaw): LanguageJsonData {
    let tempKeys = new JsonProblemKeys();
    for (const key in tempKeys) {
        console.log(key)
        if (!Array.isArray(languageJson[key]) && languageJson[key] !== null) {
            languageJson[key] = [languageJson[key]];
        };
    }
    return (languageJson as LanguageJsonData);
}

class MainLanguageList {
    langList: LanguageJsonData[];

    constructor(languageJson: LanguageJsonRecordRaw) {
        this.langList = [];
        for (const key in languageJson) {
            let newEntry: Omit<LanguageJsonData, 'name'> = fixJsonDataProperty(languageJson[key])
            const item: LanguageJsonRecord = {name: key, ...newEntry};
            this.langList.push(item);
        };
    };

    filterlanguages(predicate: () => boolean): LanguageJsonData[] {
        return(this.langList.filter(predicate));
    };
}

export const iDifficulty: string[] = ["easy", "medium", "hard", "very hard", "super hard", "whizkid"];
export const difficulty: string[] = ["easy", "medium", "hard", "very hard", "super hard", "whizkid"];
export const sensible: string[] = ["easy", "medium", "hard"];
export const tough: string[] = ["hard", "very hard", "super hard", "whizkid"];

export const indoEuro = ["Slavic", "Baltic", "Romance", "Germanic", "Indo-Aryan", "Iranian", "Celtic"]
export const nCongo = ["Bantu"]
export const afroAsiatic = ["Semitic"]

var languageScript;

const langList = new MainLanguageList(languages);
const validLangs: LanguageJsonData[] = langList.filterlanguages(
    () => globalThis.difficulty.includes(language.difficulty)
)
const sensiblelangs: LanguageJsonData[] = langList.filterlanguages(
    () => globalThis.sensible.includes(language.difficulty)
)

console.log("No. languages: ", Object.keys(languages).length)
console.log("No. valid languages: ", Object.keys(validlangs).length)
console.log("No. sensible languages: ", Object.keys(sensiblelangs).length)

class questionTypes {
    qTypes: string[] = ["where", "what", "name"];

    randomQ(): string {
        let randomKey: number = randomNumber(3)
        return this.qTypes[randomKey]
    }
}

