use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub enum SupportedMarkup {
    Asciidoc,
    Markdown,
    Text,
}

impl SupportedMarkup {
    // could be useful later; realized that we just add <hr/> in the meantime
    fn _seperator(&self) -> String {
        match self {
            SupportedMarkup::Asciidoc => "\n\n'''\n\n".to_string(),
            SupportedMarkup::Markdown => "\n\n---\n\n".to_string(),
            SupportedMarkup::Text => "\n\n#\n\n".to_string(),
        }
    }
}
