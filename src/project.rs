use crate::document::Document;
use serde::{Deserialize, Serialize};
use std::{
    env::current_dir,
    fs,
    path::{Path, PathBuf},
};

#[derive(Debug, Serialize, Deserialize)]
pub struct BartProject {
    pub name: String,
    pub byline: String,
    pub documents: Vec<Document>,
}

impl Default for BartProject {
    fn default() -> Self {
        BartProject {
            name: "A New Project".to_string(),
            byline: "YOUR NAME".to_string(),
            documents: Vec::new(),
        }
    }
}

impl BartProject {
    pub fn init(dir: Option<String>) {
        let project_dir = match dir {
            Some(dir) => {
                let mut current = current_dir().unwrap();
                current.push(Path::new(&dir));
                fs::create_dir(&current).expect("Unable to create directory {current}");
                current
            }
            None => current_dir().unwrap(),
        };
        let project = BartProject {
            name: project_dir// There must be a simpler way to do this
                .file_name()
                .unwrap()
                .to_str()
                .unwrap()
                .to_string(),
            ..Default::default()
        };

        project.save_with_create(project_dir);
    }

    fn save_with_create(self, mut project_dir: PathBuf) {
        let project_toml = toml::to_string(&self).unwrap();
        project_dir.push("bart");
        project_dir.set_extension("toml");
        fs::write(project_dir, project_toml)
            .expect("Unable to write configuration to {project_dir}");
    }
}
