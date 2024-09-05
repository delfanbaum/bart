use crate::document::Document;
use serde::{Deserialize, Serialize};
use std::{
    env::current_dir,
    fs,
    io::Write,
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
    pub fn init(name: Option<String>, byline: Option<String>, directory: Option<String>) {
        let project_dir = match directory {
            Some(dir) => {
                let mut current = current_dir().unwrap();
                current.push(Path::new(&dir));
                fs::create_dir(&current).expect("Unable to create directory {current}");
                current
            }
            None => current_dir().unwrap(),
        };
        let project = BartProject {
            name: name.unwrap_or(
                project_dir // There must be a simpler way to do this
                    .file_name()
                    .unwrap()
                    .to_str()
                    .unwrap()
                    .to_string(),
            ),
            byline: byline.unwrap_or("".to_string()),
            ..Default::default()
        };

        project.save_with_create(project_dir);
    }

    pub fn read_in_project() -> BartProject {
        let toml_file = get_project_toml();
        let toml = fs::read_to_string(toml_file).expect("Unable to read in project configuration");
        let project: BartProject = toml::from_str(&toml).unwrap();
        project
    }

    /// Creates a project from a file, usually for the purposes of building a file (where we may
    /// not always need/want to have a project associated, e.g., a short story in a single markdown
    /// file).
    ///
    /// TODO: pull in any config from the project TOML if present, e.g., custom styling
    pub fn from_file(file: String) -> BartProject {
        let fp: PathBuf = [file].iter().collect();
        assert!(fp.is_file());
        BartProject {
            name: fp.file_name().unwrap().to_str().unwrap().to_string(),
            documents: vec![Document {
                path: fp,
                ..Default::default()
            }],
            ..Default::default()
        }
    }

    pub fn add_document(&mut self, doc: Document) {
        if !doc.path.is_file() {
            let mut f = fs::File::create(&doc.path).expect("Unable to create {doc}.");
            f.write_all("".as_bytes())
                .expect("Unable to write to {doc}.");
        }
        self.documents.push(doc);
        self.save()
    }

    fn save(&self) {
        let project_toml = toml::to_string(&self).unwrap();
        let toml_file = get_project_toml();
        assert!(toml_file.is_file()); // only save inside a project directory
        fs::write(toml_file, project_toml).expect("Unable to write configuration to {project_dir}");
    }

    fn save_with_create(self, mut project_dir: PathBuf) {
        let project_toml = toml::to_string(&self).unwrap();
        project_dir.push("bart");
        project_dir.set_extension("toml");
        fs::write(project_dir, project_toml)
            .expect("Unable to write configuration to {project_dir}");
    }
}

// Assumes you're in the project directory
fn get_project_toml() -> PathBuf {
    let mut project_toml = current_dir().unwrap();
    project_toml.push("bart");
    project_toml.set_extension("toml");
    project_toml
}
