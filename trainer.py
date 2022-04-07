import torch as torch
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint
from torch.utils.data import DataLoader
from cbot import Model
import config
from dataloader import get_loader


def main():
    # Setting device
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    # Getting Data Loaders
    train_loader, val_loader, test_loader = get_loader()

    # Creating model Object
    model = Model()
    model.to(device)

    checkpoint_callback = ModelCheckpoint(
        monitor="val_loss",
        dirpath=config.weight_path,
        filename="cbot-{epoch:02d}-{val_loss:.2f}",
        save_top_k=3,
        mode="min",
    )

    # Create Trainer object
    if device.type == 'cpu':
        trainer = Trainer(max_epochs=config.epoch,
                          weights_save_path=config.weight_path,
                          callbacks=[checkpoint_callback],
                          # logger=wandb_logger,
                          precision=16
                          )
    else:
        trainer = Trainer(gpus=config.gpu_option,
                          max_epochs=config.epoch,
                          weights_save_path=config.weight_path,
                          callbacks=[checkpoint_callback],
                          # logger=wandb_logger,
                          precision=16
                          )

    # Train the Model
    trainer.fit(model=model, train_dataloaders=train_loader, val_dataloaders=val_loader, ckpt_path=config.checkpoint)


if __name__ == "__main__":
    main()
